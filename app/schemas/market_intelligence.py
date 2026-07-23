"""Output contract for the Market Intelligence Agent (mermaid nodes M1-M9)."""

from __future__ import annotations

from pydantic import BaseModel, Field


class Competitor(BaseModel):
    name: str
    notes: str = Field(description="Why this competitor is relevant, in one or two sentences.")


class MarketIntelligenceReport(BaseModel):
    """Structured research summary handed off to the Campaign Strategy Agent."""

    target_audience: str = Field(description="The audience identified or confirmed through research.")
    competitors: list[Competitor] = Field(default_factory=list, max_length=6)
    market_trends: list[str] = Field(default_factory=list, max_length=8)
    key_insights: list[str] = Field(default_factory=list, max_length=8)
    summary: str = Field(description="A short narrative synthesis of the research.")
    search_queries_used: list[str] = Field(default_factory=list)
    sources: list[str] = Field(default_factory=list, description="URLs the research drew from, if any.")
