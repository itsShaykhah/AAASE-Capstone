"""Prompts for the Campaign Strategy Agent (mermaid S1-S7)."""

from __future__ import annotations

from app.schemas.campaign_request import CampaignRequest
from app.schemas.market_intelligence import MarketIntelligenceReport


def build_system_prompt() -> str:
    return (
        "You are the Campaign Strategy Agent on an AI marketing team. Turn market "
        "research into a concrete, actionable campaign strategy: a clear goal, the "
        "channels to use, a short content calendar, content themes, and a budget "
        "split across channels that sums to 100. Be specific and realistic for a "
        "small-to-mid-size marketing budget."
    )


def build_user_prompt(request: CampaignRequest, research: MarketIntelligenceReport) -> str:
    duration = request.campaign_duration_days or 14
    return (
        f"Product: {request.product_name} — {request.product_description}\n"
        f"Campaign objective: {request.campaign_objective.value}\n"
        f"Campaign duration: {duration} days\n\n"
        f"Target audience: {research.target_audience}\n"
        f"Competitors: {', '.join(c.name for c in research.competitors) or 'none identified'}\n"
        f"Market trends: {'; '.join(research.market_trends) or 'none identified'}\n"
        f"Key insights: {'; '.join(research.key_insights) or 'none identified'}\n\n"
        "Produce the campaign strategy as the requested JSON structure. Content "
        f"calendar day numbers must stay within 1-{duration}."
    )
