"""Request validation (mermaid node GR1).

Pydantic (see app/schemas/campaign_request.py) already enforces types and
length limits. This module adds the business-rule checks that don't belong
in a schema: content that's technically valid but too degenerate to send
to an LLM (e.g. a description that's just a repeated character).
"""

from __future__ import annotations

import re

from app.guardrails.exceptions import RequestValidationError
from app.schemas.campaign_request import CampaignRequest

_MIN_MEANINGFUL_WORDS = 3
_WORD_PATTERN = re.compile(r"[A-Za-z0-9]{2,}")


def validate_campaign_request(request: CampaignRequest) -> None:
    """Raise RequestValidationError if the request is degenerate or unusable.

    This runs after Pydantic parsing, so `request` is already well-typed;
    this only checks things Pydantic can't express as a field constraint.
    """
    words = _WORD_PATTERN.findall(request.product_description)
    if len(words) < _MIN_MEANINGFUL_WORDS:
        raise RequestValidationError(
            "product_description must contain at least a few descriptive words."
        )

    if len(set(request.product_description.lower())) <= 3:
        raise RequestValidationError(
            "product_description looks degenerate (too few distinct characters)."
        )

    if request.campaign_duration_days is not None and request.campaign_duration_days < 1:
        raise RequestValidationError("campaign_duration_days must be a positive number of days.")
