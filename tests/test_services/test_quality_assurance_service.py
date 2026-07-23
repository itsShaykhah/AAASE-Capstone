"""QualityAssuranceService owns the deterministic, code-only formatting
fixes and the guardrail_validation check — the parts of QA that must hold
regardless of what any LLM says. These run in mock_mode so no network or
API key is involved.
"""

from __future__ import annotations

from app.llm.factory import LLMFactory
from app.observability.context import ObservabilityContext
from app.schemas.campaign_strategy import CampaignStrategy
from app.schemas.content_package import BrandVoice, ContentPackage, EmailCampaign
from app.services.quality_assurance_service import QualityAssuranceService


def _make_content(hashtags: list[str], x_post: str, call_to_action: str = "Shop now") -> ContentPackage:
    # Built with model_construct: it bypasses Pydantic validation, standing
    # in for content that reached this service without going through the
    # schema's own constraints (e.g. field limits changed upstream). That's
    # exactly the case the deterministic fixes below exist to still catch.
    return ContentPackage.model_construct(
        brand_voice=BrandVoice(tone="friendly", voice_description="warm and clear"),
        instagram_caption="Check this out!",
        x_post=x_post,
        linkedin_post="We're excited to announce our new product.",
        email_campaign=EmailCampaign(subject_line="Hello", body="Body text"),
        ad_headlines=["Try it today"],
        hashtags=hashtags,
        call_to_action=call_to_action,
    )


def _make_strategy() -> CampaignStrategy:
    return CampaignStrategy(campaign_goal="Drive awareness", strategy_summary="Multi-channel push")


def test_hashtags_get_normalized_and_x_post_gets_trimmed(mock_settings):
    service = QualityAssuranceService(LLMFactory(mock_settings), mock_settings)
    content = _make_content(hashtags=["no hash", "#already-good"], x_post="x" * 300)

    review = service.review(_make_strategy(), content, ObservabilityContext())

    assert all(tag.startswith("#") for tag in review.final_content.hashtags)
    assert " " not in review.final_content.hashtags[0]
    assert len(review.final_content.x_post) <= 280


def test_guardrail_validation_check_flags_missing_cta(mock_settings):
    service = QualityAssuranceService(LLMFactory(mock_settings), mock_settings)
    content = _make_content(hashtags=["#ok"], x_post="short", call_to_action="")

    review = service.review(_make_strategy(), content, ObservabilityContext())

    guardrail_check = next(c for c in review.checks if c.check_name == "guardrail_validation")
    assert guardrail_check.status.value == "needs_attention"
    assert "call_to_action is empty" in guardrail_check.notes
