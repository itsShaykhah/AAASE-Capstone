"""Unit tests for the MarketIntelligenceAgent adapter, using a stub service
so these tests never touch an LLM or the network — they only check that
the agent correctly bridges graph state <-> service calls, including its
last-resort fallback when the service raises unexpectedly.
"""

from __future__ import annotations

from app.agents.market_intelligence_agent import MarketIntelligenceAgent
from app.observability.context import ObservabilityContext
from app.schemas.campaign_request import CampaignRequest
from app.schemas.enums import CampaignObjective
from app.schemas.market_intelligence import MarketIntelligenceReport


class _StubService:
    def __init__(self, report: MarketIntelligenceReport | None = None, exc: Exception | None = None) -> None:
        self._report = report
        self._exc = exc

    def generate(self, request, observability):
        if self._exc:
            raise self._exc
        return self._report


def _make_request() -> CampaignRequest:
    return CampaignRequest(
        product_name="Acme Widget",
        product_description="A durable widget that helps small teams ship faster.",
        campaign_objective=CampaignObjective.BRAND_AWARENESS,
    )


def test_agent_returns_service_output_on_success():
    report = MarketIntelligenceReport(target_audience="Ops teams", summary="Looks promising.")
    agent = MarketIntelligenceAgent(_StubService(report=report))
    state = {"request": _make_request(), "observability": ObservabilityContext()}

    update = agent.run(state)

    assert update["market_intelligence"] is report
    assert "errors" not in update


def test_agent_falls_back_and_records_error_on_unexpected_exception():
    agent = MarketIntelligenceAgent(_StubService(exc=RuntimeError("boom")))
    state = {"request": _make_request(), "observability": ObservabilityContext()}

    update = agent.run(state)

    assert update["market_intelligence"].target_audience
    assert "unhandled error" in update["errors"][0]
