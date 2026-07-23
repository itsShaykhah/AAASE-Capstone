"""Prompts for the Market Intelligence Agent (mermaid M5-M9 synthesis step)."""

from __future__ import annotations

from app.schemas.campaign_request import CampaignRequest


def build_system_prompt() -> str:
    return (
        "You are the Market Intelligence Agent on an AI marketing team. Given a "
        "product brief and real web search results, identify the target audience, "
        "key competitors, and current market trends. Ground claims in the search "
        "results where possible; where they're thin, rely on sound general "
        "marketing knowledge and say so implicitly by keeping claims general. "
        "Be concise and concrete — no filler."
    )


def build_user_prompt(request: CampaignRequest, search_digest: str) -> str:
    return (
        f"Product name: {request.product_name}\n"
        f"Product description: {request.product_description}\n"
        f"Campaign objective: {request.campaign_objective.value}\n"
        f"User-provided target audience (may be unspecified): {request.target_audience or 'not specified'}\n\n"
        f"Web search findings:\n{search_digest}\n\n"
        "Synthesize this into the requested JSON structure."
    )
