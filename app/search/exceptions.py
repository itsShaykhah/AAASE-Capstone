"""Exception types for the search layer."""

from __future__ import annotations


class SearchProviderError(Exception):
    """A single search provider failed (network error, bad key, rate limit)."""


class SearchUnavailableError(Exception):
    """Both the primary and fallback search providers failed."""
