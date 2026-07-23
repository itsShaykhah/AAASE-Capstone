"""Business logic for the Market Intelligence Agent (mermaid M1-M9).

Flow: build a few targeted search queries (M2) -> run them through
SearchService, which handles the Tavily->Serper fallback itself (M3/M4) ->
ask the LLM to synthesize audience/competitors/trends/insights from the
findings (M5-M8) into a MarketIntelligenceReport (M9).
"""

from __future__ import annotations

from app.config.settings import Settings
from app.guardrails.exceptions import OutputValidationError
from app.llm.exceptions import LLMInvocationError
from app.llm.factory import LLMFactory
from app.llm.fallback_content import fallback_market_intelligence
from app.llm.structured_output import generate_structured_response
from app.observability.context import ObservabilityContext
from app.observability.event_logger import EventLogger
from app.prompts.market_intelligence import build_system_prompt, build_user_prompt
from app.schemas.campaign_request import CampaignRequest
from app.schemas.enums import AgentKey
from app.schemas.market_intelligence import MarketIntelligenceReport
from app.search.exceptions import SearchUnavailableError
from app.search.schemas import SearchResponse
from app.search.service import SearchService

_MAX_SOURCES = 10
_MAX_SNIPPETS_PER_QUERY = 5


class MarketIntelligenceService:
    def __init__(self, llm_factory: LLMFactory, search_service: SearchService, settings: Settings) -> None:
        self._llm_factory = llm_factory
        self._search_service = search_service
        self._settings = settings

    def generate(
        self, request: CampaignRequest, observability: ObservabilityContext
    ) -> MarketIntelligenceReport:
        with observability.observe_agent(AgentKey.MARKET_INTELLIGENCE) as agent_context:
            if self._settings.mock_mode:
                agent_context["provider"] = "mock"
                return fallback_market_intelligence(request)

            queries = self._build_search_queries(request)
            search_digest, sources = self._run_searches(queries, observability.event_logger)

            try:
                report, llm_config = generate_structured_response(
                    llm_factory=self._llm_factory,
                    agent_key=AgentKey.MARKET_INTELLIGENCE,
                    system_prompt=build_system_prompt(),
                    user_prompt=build_user_prompt(request, search_digest),
                    schema=MarketIntelligenceReport,
                    max_retries=self._settings.llm_max_retries,
                )
            except (OutputValidationError, LLMInvocationError) as exc:
                observability.metrics.record_error(f"{AgentKey.MARKET_INTELLIGENCE.value}: {exc}")
                observability.event_logger.log(
                    "agent_degraded", agent=AgentKey.MARKET_INTELLIGENCE.value, reason=str(exc)
                )
                agent_context["provider"] = "fallback"
                report = fallback_market_intelligence(request)
            else:
                agent_context["provider"] = f"{llm_config.provider.value}:{llm_config.model}"

            report.search_queries_used = queries
            report.sources = sources
            return report

    def _build_search_queries(self, request: CampaignRequest) -> list[str]:
        """M2 — Generate Optimized Search Queries.

        Deterministic templates rather than an extra LLM call: three
        focused queries are enough signal for the synthesis step and keep
        this agent to a single LLM call overall.
        """
        objective_phrase = request.campaign_objective.value.replace("_", " ")
        return [
            f"{request.product_name} competitors",
            f"{request.product_name} target audience",
            f"marketing trends for {objective_phrase} campaigns",
        ]

    def _run_searches(
        self, queries: list[str], event_logger: EventLogger
    ) -> tuple[str, list[str]]:
        """M3/M4 — run each query through SearchService and build a text
        digest the LLM can read, plus a flat list of source URLs."""
        digest_sections: list[str] = []
        sources: list[str] = []

        for query in queries:
            try:
                response = self._search_service.search(query, event_logger=event_logger)
            except SearchUnavailableError as exc:
                event_logger.log("search_unavailable", query=query, error=str(exc))
                continue

            digest_sections.append(self._format_search_response(response))
            sources.extend(item.url for item in response.results if item.url)

        digest = "\n\n".join(digest_sections) or "No search results were available for this run."
        return digest, sources[:_MAX_SOURCES]

    @staticmethod
    def _format_search_response(response: SearchResponse) -> str:
        lines = [f"Query: {response.query} (via {response.provider})"]
        for item in response.results[:_MAX_SNIPPETS_PER_QUERY]:
            lines.append(f"- {item.title}: {item.snippet}")
        return "\n".join(lines)
