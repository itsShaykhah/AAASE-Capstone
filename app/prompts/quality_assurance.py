"""Prompts for the Quality Assurance Agent (mermaid Q1-Q7).

The model is asked only for an assessment (pass/fail per check + notes),
never to rewrite the content itself — see app/schemas/quality_review.py
for why. Deterministic formatting fixes happen in code after this call.
"""

from __future__ import annotations

from app.schemas.campaign_strategy import CampaignStrategy
from app.schemas.content_package import ContentPackage


def build_system_prompt() -> str:
    return (
        "You are the Quality Assurance Agent on an AI marketing team. Review a "
        "generated marketing content package for: brand voice consistency across "
        "assets, tone appropriateness for each platform, grammar/spelling, and "
        "overall marketing quality (clarity, a genuine call-to-action, no empty "
        "hype). Report one check result per dimension and an overall approval "
        "decision. Only withhold approval for real problems, not stylistic taste."
    )


def build_user_prompt(strategy: CampaignStrategy, content: ContentPackage) -> str:
    return (
        f"Campaign goal: {strategy.campaign_goal}\n"
        f"Intended brand voice: {content.brand_voice.tone} — {content.brand_voice.voice_description}\n\n"
        f"Instagram caption: {content.instagram_caption}\n"
        f"X post: {content.x_post}\n"
        f"LinkedIn post: {content.linkedin_post}\n"
        f"Email subject: {content.email_campaign.subject_line}\n"
        f"Email body: {content.email_campaign.body}\n"
        f"Ad headlines: {'; '.join(content.ad_headlines)}\n"
        f"Hashtags: {' '.join(content.hashtags)}\n"
        f"Call to action: {content.call_to_action}\n\n"
        "Assess this package as the requested JSON structure. Use check_name values: "
        "'brand_consistency', 'tone_validation', 'grammar_review', 'marketing_quality'."
    )
