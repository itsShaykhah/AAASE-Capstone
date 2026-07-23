"""Search layer used exclusively by the Market Intelligence Agent.

Per the architecture, only market research needs live web search — every
other agent works from structured outputs earlier agents produced. Keeping
search isolated here (behind `SearchService`) means the rest of the system
never imports `tavily` or `requests` directly, and a third search provider
can be added without touching the agent that uses it.
"""

from app.search.schemas import SearchResponse, SearchResultItem
from app.search.service import SearchService

__all__ = ["SearchService", "SearchResponse", "SearchResultItem"]
