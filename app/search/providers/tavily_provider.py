"""Tavily search provider — the primary search source (mermaid node M3).

Tavily is purpose-built for LLM-facing search (it returns clean summarized
content rather than raw SERP HTML), which is why it's primary and Serper is
the fallback rather than the other way around.
"""

from __future__ import annotations

from tavily import TavilyClient

from app.search.exceptions import SearchProviderError
from app.search.providers.base import BaseSearchProvider
from app.search.schemas import SearchResponse, SearchResultItem


class TavilyProvider(BaseSearchProvider):
    name = "tavily"

    def __init__(self, api_key: str) -> None:
        self._client = TavilyClient(api_key=api_key)

    def search(self, query: str, max_results: int) -> SearchResponse:
        try:
            raw = self._client.search(query=query, max_results=max_results)
        except Exception as exc:  # noqa: BLE001 - the SDK raises various HTTP/network errors
            raise SearchProviderError(f"Tavily search failed: {exc}") from exc

        results = [
            SearchResultItem(
                title=item.get("title", ""),
                url=item.get("url", ""),
                snippet=item.get("content", ""),
            )
            for item in raw.get("results", [])
        ]
        return SearchResponse(query=query, provider=self.name, results=results)
