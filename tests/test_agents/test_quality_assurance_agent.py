"""Unit tests for the QualityAssuranceAgent adapter's fallback safety net."""

from __future__ import annotations

from app.agents.quality_assurance_agent import QualityAssuranceAgent
from app.observability.context import ObservabilityContext
from app.schemas.content_package import BrandVoice, ContentPackage, EmailCampaign


class _RaisingService:
    def review(self, strategy, content, observability):
        raise RuntimeError("QA model unavailable")


def _make_content() -> ContentPackage:
    return ContentPackage(
        brand_voice=BrandVoice(tone="friendly", voice_description="warm and clear"),
        instagram_caption="Check this out!",
        x_post="Announcing our new product.",
        linkedin_post="We're excited to announce our new product.",
        email_campaign=EmailCampaign(subject_line="Hello", body="Body text"),
        ad_headlines=["Try it today"],
        hashtags=["#new"],
        call_to_action="Shop now",
    )


def test_agent_falls_back_when_service_raises_unexpectedly():
    agent = QualityAssuranceAgent(_RaisingService())
    state = {
        "campaign_strategy": None,
        "content_package": _make_content(),
        "observability": ObservabilityContext(),
    }

    update = agent.run(state)

    assert update["quality_review"].final_content == _make_content()
    assert "unhandled error" in update["errors"][0]
