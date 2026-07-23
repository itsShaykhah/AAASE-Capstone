"""Exception types for the guardrail layer.

Kept separate from the check logic so agents/API code can catch a specific
guardrail failure (e.g. to return HTTP 422 vs 502) without importing the
modules that raise them.
"""

from __future__ import annotations


class GuardrailViolation(Exception):
    """Base class for any guardrail rejecting a request or output."""


class RequestValidationError(GuardrailViolation):
    """The incoming CampaignRequest failed a business-rule check."""


class PromptInjectionDetected(GuardrailViolation):
    """User-supplied free text matched a known prompt-injection pattern."""

    def __init__(self, matched_patterns: list[str]) -> None:
        self.matched_patterns = matched_patterns
        super().__init__(f"Prompt injection patterns detected: {matched_patterns}")


class OutputValidationError(GuardrailViolation):
    """An LLM response could not be parsed/validated against its schema."""
