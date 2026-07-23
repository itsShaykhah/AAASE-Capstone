"""Provider interface every search adapter must implement."""

from __future__ import annotations

from abc import ABC, abstractmethod

from app.search.schemas import SearchResponse


class BaseSearchProvider(ABC):
    name: str

    @abstractmethod
    def search(self, query: str, max_results: int) -> SearchResponse:
        """Run one query and return normalized results.

        Implementations should raise `app.search.exceptions.SearchProviderError`
        on any failure (bad key, timeout, non-2xx response) so `SearchService`
        can uniformly decide whether to fall back.
        """
        raise NotImplementedError
