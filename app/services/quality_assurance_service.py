"""Business logic for the Quality Assurance Agent (mermaid Q1-Q7).

Two things happen here, deliberately kept separate:

1. An LLM call asks for an *assessment only* (per-dimension pass/fail +
   notes) — see app/schemas/quality_review.py for why the model never
   rewrites the content itself.
2. Deterministic, code-only fixes (hashtag formatting, X-post length) and a
   final guardrail_validation check run on every campaign regardless of
   whether the LLM call succeeded, so structural correctness never depends
   on model behavior.
"""

from __future__ import annotations

from app.config.settings import Settings
from app.guardrails.exceptions import OutputValidationError
from app.llm.exceptions import LLMInvocationError
from app.llm.factory import LLMFactory
from app.llm.fallback_content import fallback_quality_review
from app.llm.structured_output import generate_structured_response
from app.observability.context import ObservabilityContext
from app.prompts.quality_assurance import build_system_prompt, build_user_prompt
from app.schemas.campaign_strategy import CampaignStrategy
from app.schemas.content_package import ContentPackage
from app.schemas.enums import AgentKey, QualityCheckStatus
from app.schemas.quality_review import QualityAssessment, QualityCheckResult, QualityReview

_X_POST_LIMIT = 280


class QualityAssuranceService:
    def __init__(self, llm_factory: LLMFactory, settings: Settings) -> None:
        self._llm_factory = llm_factory
        self._settings = settings

    def review(
        self,
        strategy: CampaignStrategy,
        content: ContentPackage,
        observability: ObservabilityContext,
    ) -> QualityReview:
        fixed_content = self._apply_deterministic_fixes(content)
        guardrail_check = self._guardrail_validation_check(fixed_content)

        with observability.observe_agent(AgentKey.QUALITY_ASSURANCE) as agent_context:
            if self._settings.mock_mode:
                agent_context["provider"] = "mock"
                review = fallback_quality_review(fixed_content)
                review.checks.append(guardrail_check)
                return review

            try:
                assessment, llm_config = generate_structured_response(
                    llm_factory=self._llm_factory,
                    agent_key=AgentKey.QUALITY_ASSURANCE,
                    system_prompt=build_system_prompt(),
                    user_prompt=build_user_prompt(strategy, fixed_content),
                    schema=QualityAssessment,
                    max_retries=self._settings.llm_max_retries,
                )
            except (OutputValidationError, LLMInvocationError) as exc:
                observability.metrics.record_error(f"{AgentKey.QUALITY_ASSURANCE.value}: {exc}")
                observability.event_logger.log(
                    "agent_degraded", agent=AgentKey.QUALITY_ASSURANCE.value, reason=str(exc)
                )
                agent_context["provider"] = "fallback"
                review = fallback_quality_review(fixed_content)
                review.checks.append(guardrail_check)
                return review

            agent_context["provider"] = f"{llm_config.provider.value}:{llm_config.model}"
            return QualityReview(
                checks=[*assessment.checks, guardrail_check],
                overall_approved=assessment.overall_approved and guardrail_check.status != QualityCheckStatus.FAILED,
                final_notes=assessment.final_notes,
                final_content=fixed_content,
            )

    def _apply_deterministic_fixes(self, content: ContentPackage) -> ContentPackage:
        """Q6-adjacent formatting fixes that don't need a model: normalize
        hashtags and enforce the X character limit."""
        fixed = content.model_copy(deep=True)
        fixed.hashtags = [
            ("#" + tag.lstrip("#")).replace(" ", "") for tag in fixed.hashtags if tag.strip()
        ]
        if len(fixed.x_post) > _X_POST_LIMIT:
            fixed.x_post = fixed.x_post[: _X_POST_LIMIT - 3].rstrip() + "..."
        return fixed

    def _guardrail_validation_check(self, content: ContentPackage) -> QualityCheckResult:
        """Q6 — Guardrail Validation: structural checks independent of the LLM."""
        issues: list[str] = []
        if len(content.x_post) > _X_POST_LIMIT:
            issues.append("x_post exceeds the 280 character limit")
        if not content.call_to_action.strip():
            issues.append("call_to_action is empty")
        if not content.hashtags:
            issues.append("no hashtags were generated")

        status = QualityCheckStatus.PASSED if not issues else QualityCheckStatus.NEEDS_ATTENTION
        return QualityCheckResult(
            check_name="guardrail_validation",
            status=status,
            notes="; ".join(issues) or "All structural guardrails passed.",
        )
