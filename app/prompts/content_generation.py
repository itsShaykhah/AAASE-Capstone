"""Prompts for the Content Generation Agent (mermaid C1-C11).

Note: this agent generates copy for review, it does not publish anything —
the prompt says so explicitly so the model doesn't imply the post already
went live.
"""

from __future__ import annotations

from app.schemas.campaign_request import CampaignRequest
from app.schemas.campaign_strategy import CampaignStrategy


def build_system_prompt() -> str:
    return (
        "You are the Content Generation Agent on an AI marketing team. Write a "
        "complete, platform-specific marketing content package for a human to "
        "review, edit, and publish themselves — you are not publishing anything. "
        "Keep a single consistent brand voice across every asset. Respect platform "
        "conventions: the X post must fit in 280 characters, the Instagram caption "
        "should feel native to Instagram, the LinkedIn post should be more "
        "professional, and the email should have a genuine subject line and body."
    )


def build_user_prompt(request: CampaignRequest, strategy: CampaignStrategy) -> str:
    tone_hint = request.brand_tone or "confident, friendly, and clear"
    return (
        f"Product: {request.product_name} — {request.product_description}\n"
        f"Campaign goal: {strategy.campaign_goal}\n"
        f"Content themes: {', '.join(strategy.content_themes) or 'none specified'}\n"
        f"Channels in use: {', '.join(strategy.marketing_channels)}\n"
        f"Desired brand tone: {tone_hint}\n\n"
        "Produce the full content package as the requested JSON structure."
    )
