"""SearchService — Tavily primary, Serper fallback (mermaid M3 -> M4).

This is the only object the Market Intelligence Agent talks to for web
search. It hides both which provider answered and the fallback decision,
so the agent's logic is "search for this query" rather than "try Tavily,
catch its errors, try Serper."
"""

from __future__ import annotations

from app.config.settings import Settings
from app.observability.event_logger import EventLogger
from app.search.exceptions import SearchProviderError, SearchUnavailableError
from app.search.providers.base import BaseSearchProvider
from app.search.providers.serper_provider import SerperProvider
from app.search.providers.tavily_provider import TavilyProvider
from app.search.schemas import SearchResponse


class SearchService:
    def __init__(self, settings: Settings) -> None:
        self._settings = settings
        self._primary: BaseSearchProvider | None = (
            TavilyProvider(api_key=settings.tavily_api_key) if settings.tavily_api_key else None
        )
        self._fallback: BaseSearchProvider | None = (
            SerperProvider(api_key=settings.serper_api_key, timeout_seconds=settings.search_request_timeout_seconds)
            if settings.serper_api_key
            else None
        )

    def search(self, query: str, event_logger: EventLogger | None = None) -> SearchResponse:
        """Run `query` against the primary provider, falling back on failure.

        Raises SearchUnavailableError only if no provider is configured, or
        every configured provider failed.
        """
        max_results = self._settings.search_max_results
        errors: list[str] = []

        for provider in (self._primary, self._fallback):
            if provider is None:
                continue
            try:
                return provider.search(query, max_results)
            except SearchProviderError as exc:
                errors.append(str(exc))
                if event_logger:
                    event_logger.log("search_provider_failed", provider=provider.name, error=str(exc))

        if errors:
            raise SearchUnavailableError(
                "All configured search providers failed: " + "; ".join(errors)
            )
        raise SearchUnavailableError("No search provider (Tavily/Serper) is configured.")
