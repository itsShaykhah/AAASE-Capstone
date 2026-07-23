"""Serper search provider — the fallback search source (mermaid node M4).

Serper wraps Google Search results. It's kept as a plain `requests` call
rather than an SDK dependency since its API surface is a single JSON POST.
"""

from __future__ import annotations

import requests

from app.search.exceptions import SearchProviderError
from app.search.providers.base import BaseSearchProvider
from app.search.schemas import SearchResponse, SearchResultItem

_SERPER_ENDPOINT = "https://google.serper.dev/search"


class SerperProvider(BaseSearchProvider):
    name = "serper"

    def __init__(self, api_key: str, timeout_seconds: int) -> None:
        self._api_key = api_key
        self._timeout_seconds = timeout_seconds

    def search(self, query: str, max_results: int) -> SearchResponse:
        try:
            response = requests.post(
                _SERPER_ENDPOINT,
                headers={"X-API-KEY": self._api_key, "Content-Type": "application/json"},
                json={"q": query, "num": max_results},
                timeout=self._timeout_seconds,
            )
            response.raise_for_status()
            payload = response.json()
        except Exception as exc:  # noqa: BLE001 - network/HTTP errors of many types
            raise SearchProviderError(f"Serper search failed: {exc}") from exc

        results = [
            SearchResultItem(
                title=item.get("title", ""),
                url=item.get("link", ""),
                snippet=item.get("snippet", ""),
            )
            for item in payload.get("organic", [])[:max_results]
        ]
        return SearchResponse(query=query, provider=self.name, results=results)
