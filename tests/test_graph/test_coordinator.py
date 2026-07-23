"""End-to-end test of the compiled LangGraph pipeline in mock mode.

This is the test that proves the whole system — routing between all four
agents, state accumulation, and observability — actually works together,
without needing any API key or network access.
"""

from __future__ import annotations

from app.graph.coordinator import CampaignCoordinator
from app.schemas.campaign_request import CampaignRequest
from app.schemas.enums import CampaignObjective, CampaignStatus


def test_full_pipeline_runs_end_to_end_in_mock_mode(mock_settings):
    coordinator = CampaignCoordinator(mock_settings)
    request = CampaignRequest(
        product_name="Acme Widget",
        product_description="A durable widget that helps small teams ship faster.",
        campaign_objective=CampaignObjective.PRODUCT_LAUNCH,
        campaign_duration_days=14,
    )

    result = coordinator.run(request)

    assert result.status == CampaignStatus.COMPLETED
    assert result.market_intelligence is not None
    assert result.campaign_strategy is not None
    assert result.content_package is not None
    assert result.quality_review is not None
    assert result.quality_review.final_content.call_to_action

    assert result.observability.total_duration_ms >= 0
    assert len(result.observability.agent_durations_ms) == 4
    assert set(result.observability.provider_used.values()) == {"mock"}
