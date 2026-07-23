"""GuardrailManager — the single pre-flight checkpoint (mermaid G2).

This is what the API layer calls between Request Validation (FastAPI's own
Pydantic parsing, GR1) and handing the request to the Coordinator. It
combines the business-rule and prompt-injection checks into one call so
the API route doesn't need to know how many individual guardrails exist.
"""

from __future__ import annotations

from app.guardrails.exceptions import PromptInjectionDetected
from app.guardrails.prompt_injection import detect_prompt_injection
from app.guardrails.request_validation import validate_campaign_request
from app.schemas.campaign_request import CampaignRequest

_FREE_TEXT_FIELDS = ("product_description", "target_audience", "brand_tone", "additional_notes")


class GuardrailManager:
    """Runs all pre-execution guardrails against an incoming request."""

    def run_pre_checks(self, request: CampaignRequest) -> None:
        """Validate `request`, raising a GuardrailViolation subclass on failure."""
        validate_campaign_request(request)

        matched: list[str] = []
        for field_name in _FREE_TEXT_FIELDS:
            value = getattr(request, field_name)
            if value:
                matched.extend(detect_prompt_injection(value))

        if matched:
            raise PromptInjectionDetected(sorted(set(matched)))
