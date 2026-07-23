"""CampaignCoordinator — builds the StateGraph and runs one campaign.

This is the single entrypoint the API (and, indirectly, the UI) uses to
turn a CampaignRequest into a CampaignResult. It owns the composition root:
constructing the LLM factory, search service, per-agent services, and
agents, then wiring them into a linear LangGraph StateGraph that mirrors
the architecture diagram exactly —

    START -> market_intelligence -> campaign_strategy
          -> content_generation -> quality_assurance -> END

Constructing everything in one place (rather than each agent reaching for
a global) is what makes the system testable: a test can build a
CampaignCoordinator with a Settings object pointed at mock mode and get a
fully isolated pipeline.
"""

from __future__ import annotations

from langgraph.graph import END, START, StateGraph

from app.agents.campaign_strategy_agent import CampaignStrategyAgent
from app.agents.content_generation_agent import ContentGenerationAgent
from app.agents.market_intelligence_agent import MarketIntelligenceAgent
from app.agents.quality_assurance_agent import QualityAssuranceAgent
from app.config.settings import Settings, get_settings
from app.graph.nodes import make_node
from app.llm.factory import LLMFactory
from app.observability.context import ObservabilityContext
from app.schemas.campaign_request import CampaignRequest
from app.schemas.campaign_result import CampaignResult, ObservabilitySummary
from app.schemas.enums import AgentKey, CampaignStatus
from app.schemas.graph_state import CampaignGraphState
from app.search.service import SearchService
from app.services.campaign_strategy_service import CampaignStrategyService
from app.services.content_generation_service import ContentGenerationService
from app.services.market_intelligence_service import MarketIntelligenceService
from app.services.quality_assurance_service import QualityAssuranceService


class CampaignCoordinator:
    """Compiles and runs the four-agent campaign generation pipeline."""

    def __init__(self, settings: Settings | None = None) -> None:
        self._settings = settings or get_settings()

        llm_factory = LLMFactory(self._settings)
        search_service = SearchService(self._settings)

        market_intelligence_agent = MarketIntelligenceAgent(
            MarketIntelligenceService(llm_factory, search_service, self._settings)
        )
        campaign_strategy_agent = CampaignStrategyAgent(
            CampaignStrategyService(llm_factory, self._settings)
        )
        content_generation_agent = ContentGenerationAgent(
            ContentGenerationService(llm_factory, self._settings)
        )
        quality_assurance_agent = QualityAssuranceAgent(
            QualityAssuranceService(llm_factory, self._settings)
        )

        self._compiled_graph = self._build_graph(
            market_intelligence_agent,
            campaign_strategy_agent,
            content_generation_agent,
            quality_assurance_agent,
        )

    @staticmethod
    def _build_graph(
        market_intelligence_agent: MarketIntelligenceAgent,
        campaign_strategy_agent: CampaignStrategyAgent,
        content_generation_agent: ContentGenerationAgent,
        quality_assurance_agent: QualityAssuranceAgent,
    ):
        graph = StateGraph(CampaignGraphState)

        graph.add_node(AgentKey.MARKET_INTELLIGENCE.value, make_node(AgentKey.MARKET_INTELLIGENCE.value, market_intelligence_agent))
        graph.add_node(AgentKey.CAMPAIGN_STRATEGY.value, make_node(AgentKey.CAMPAIGN_STRATEGY.value, campaign_strategy_agent))
        graph.add_node(AgentKey.CONTENT_GENERATION.value, make_node(AgentKey.CONTENT_GENERATION.value, content_generation_agent))
        graph.add_node(AgentKey.QUALITY_ASSURANCE.value, make_node(AgentKey.QUALITY_ASSURANCE.value, quality_assurance_agent))

        graph.add_edge(START, AgentKey.MARKET_INTELLIGENCE.value)
        graph.add_edge(AgentKey.MARKET_INTELLIGENCE.value, AgentKey.CAMPAIGN_STRATEGY.value)
        graph.add_edge(AgentKey.CAMPAIGN_STRATEGY.value, AgentKey.CONTENT_GENERATION.value)
        graph.add_edge(AgentKey.CONTENT_GENERATION.value, AgentKey.QUALITY_ASSURANCE.value)
        graph.add_edge(AgentKey.QUALITY_ASSURANCE.value, END)

        return graph.compile()

    def run(self, request: CampaignRequest) -> CampaignResult:
        """Run the full pipeline for one CampaignRequest and return the result.

        A hard failure (an exception escaping all four agents' own
        safety nets) is still reported as a CampaignResult with
        status=FAILED rather than raised, so the API/UI always get a
        well-formed response to render.
        """
        observability = ObservabilityContext()
        initial_state: CampaignGraphState = {
            "trace_id": observability.trace_id,
            "request": request,
            "observability": observability,
            "errors": [],
            "execution_events": [],
        }

        try:
            final_state = self._compiled_graph.invoke(initial_state)
        except Exception as exc:  # noqa: BLE001 - top-level safety net for the whole run
            observability.event_logger.log("run_failed", error=str(exc))
            return CampaignResult(
                trace_id=observability.trace_id,
                status=CampaignStatus.FAILED,
                request=request,
                observability=self._build_observability_summary(observability),
            )

        return CampaignResult(
            trace_id=observability.trace_id,
            status=CampaignStatus.COMPLETED,
            request=request,
            market_intelligence=final_state.get("market_intelligence"),
            campaign_strategy=final_state.get("campaign_strategy"),
            content_package=final_state.get("content_package"),
            quality_review=final_state.get("quality_review"),
            observability=self._build_observability_summary(observability),
        )

    @staticmethod
    def _build_observability_summary(observability: ObservabilityContext) -> ObservabilitySummary:
        return ObservabilitySummary(
            trace_id=observability.trace_id,
            total_duration_ms=observability.total_duration_ms(),
            agent_durations_ms=observability.metrics.agent_durations_ms,
            provider_used=observability.metrics.provider_used,
            errors=observability.metrics.errors,
            events=observability.event_logger.events,
        )
