"""Unified search result shape, independent of which provider answered."""

from __future__ import annotations

from pydantic import BaseModel


class SearchResultItem(BaseModel):
    title: str
    url: str
    snippet: str = ""


class SearchResponse(BaseModel):
    query: str
    provider: str
    results: list[SearchResultItem]
