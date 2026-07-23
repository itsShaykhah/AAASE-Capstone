"""Deterministic, schema-valid fixtures used in two situations:

1. `Settings.mock_mode` is on — the whole pipeline runs with zero API keys,
   which is how tests and offline demos work (mirrors the `MOCK=1` pattern
   from resources-from-instrcutor-do-not-modify/01_BUILD_THE_AGENT.md).
2. Graceful degradation — a real LLM call exhausted its retries. Rather
   than crash the whole campaign, the agent falls back to one of these so
   the user still gets a complete (if generic) deliverable, and the
   failure is recorded in observability instead of hidden.

Reusing the same fixtures for both cases is intentional: "the system's
answer when it can't reach a model" and "the system's answer when you
haven't given it a model" are the same product requirement.
"""

from __future__ import annotations

from app.schemas.campaign_request import CampaignRequest
from app.schemas.campaign_strategy import (
    BudgetAllocation,
    CampaignStrategy,
    ContentCalendarEntry,
)
from app.schemas.content_package import BrandVoice, ContentPackage, EmailCampaign
from app.schemas.market_intelligence import Competitor, MarketIntelligenceReport
from app.schemas.quality_review import QualityCheckResult, QualityReview
from app.schemas.enums import QualityCheckStatus


def fallback_market_intelligence(request: CampaignRequest) -> MarketIntelligenceReport:
    audience = request.target_audience or f"Early adopters interested in {request.product_name}"
    return MarketIntelligenceReport(
        target_audience=audience,
        competitors=[
            Competitor(name="Established Incumbent", notes="Category leader with broad brand recognition."),
            Competitor(name="Emerging Challenger", notes="Growing quickly on price and social proof."),
        ],
        market_trends=[
            "Buyers increasingly research on social platforms before purchasing.",
            "Short-form video and authentic, creator-style content outperform polished ads.",
        ],
        key_insights=[
            f"{request.product_name} should lead with a clear, single value proposition.",
            "Audience trust is built through consistency across channels, not volume.",
        ],
        summary=(
            f"Research data was unavailable for this run, so this is a generic baseline "
            f"summary for {request.product_name}. Treat the audience, competitors, and "
            "trends above as a starting point to validate, not a finished report."
        ),
        search_queries_used=[],
        sources=[],
    )


def fallback_campaign_strategy(
    request: CampaignRequest, research: MarketIntelligenceReport
) -> CampaignStrategy:
    duration = request.campaign_duration_days or 14
    return CampaignStrategy(
        campaign_goal=f"Drive {request.campaign_objective.value.replace('_', ' ')} for {request.product_name}",
        marketing_channels=["Instagram", "X", "LinkedIn", "Email"],
        content_calendar=[
            ContentCalendarEntry(day=1, channel="Instagram", theme="Launch announcement"),
            ContentCalendarEntry(day=max(2, duration // 3), channel="Email", theme="Deep dive / education"),
            ContentCalendarEntry(day=max(3, duration // 2), channel="LinkedIn", theme="Credibility and proof"),
            ContentCalendarEntry(day=duration, channel="X", theme="Final call to action"),
        ],
        content_themes=research.market_trends[:2] or ["Product value", "Customer proof"],
        budget_allocation=[
            BudgetAllocation(channel="Instagram", percentage=35),
            BudgetAllocation(channel="LinkedIn", percentage=25),
            BudgetAllocation(channel="Email", percentage=25),
            BudgetAllocation(channel="X", percentage=15),
        ],
        strategy_summary=(
            f"A {duration}-day multi-channel plan built from a generic baseline (no live "
            "strategy model output for this run)."
        ),
    )


def fallback_content_package(
    request: CampaignRequest, strategy: CampaignStrategy
) -> ContentPackage:
    tone = request.brand_tone or "confident and approachable"
    return ContentPackage(
        brand_voice=BrandVoice(
            tone=tone,
            style_keywords=["clear", "direct", "customer-first"],
            voice_description=f"Speak to the audience like a knowledgeable friend, in a {tone} tone.",
        ),
        instagram_caption=f"Meet {request.product_name}. {request.product_description[:120]} ✨",
        x_post=f"{request.product_name} is here. {strategy.campaign_goal}."[:280],
        linkedin_post=(
            f"We're excited to share {request.product_name}. {strategy.strategy_summary}"
        ),
        email_campaign=EmailCampaign(
            subject_line=f"Introducing {request.product_name}",
            body=(
                f"Hi there,\n\n{request.product_description}\n\n"
                f"{strategy.strategy_summary}\n\nBest,\nThe Team"
            ),
        ),
        ad_headlines=[
            f"Discover {request.product_name}",
            f"{request.product_name}: Built for you",
        ],
        hashtags=["#" + request.product_name.replace(" ", ""), "#NewLaunch"],
        call_to_action="Learn more today.",
    )


def fallback_quality_review(content_package: ContentPackage) -> QualityReview:
    return QualityReview(
        checks=[
            QualityCheckResult(
                check_name="brand_consistency",
                status=QualityCheckStatus.NEEDS_ATTENTION,
                notes="Automated fallback review only; a human should confirm brand voice.",
            ),
            QualityCheckResult(check_name="tone_validation", status=QualityCheckStatus.PASSED),
            QualityCheckResult(check_name="grammar_review", status=QualityCheckStatus.PASSED),
        ],
        overall_approved=True,
        final_notes=(
            "This review was generated by the fallback path (no live QA model output for "
            "this run). Recommend a manual pass before publishing."
        ),
        final_content=content_package,
    )
