"""Output contract for the Campaign Strategy Agent (mermaid nodes S1-S7)."""

from __future__ import annotations

from pydantic import BaseModel, Field


class ContentCalendarEntry(BaseModel):
    day: int = Field(ge=1, description="Day offset from campaign start, e.g. 1 = launch day.")
    channel: str
    theme: str


class BudgetAllocation(BaseModel):
    channel: str
    percentage: float = Field(ge=0, le=100)


class CampaignStrategy(BaseModel):
    """Strategic plan handed off to the Content Generation Agent."""

    campaign_goal: str
    marketing_channels: list[str] = Field(default_factory=list, max_length=8)
    content_calendar: list[ContentCalendarEntry] = Field(default_factory=list, max_length=30)
    content_themes: list[str] = Field(default_factory=list, max_length=8)
    budget_allocation: list[BudgetAllocation] = Field(default_factory=list, max_length=8)
    strategy_summary: str
