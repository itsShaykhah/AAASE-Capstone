from __future__ import annotations

import pytest

from app.guardrails.exceptions import RequestValidationError
from app.guardrails.request_validation import validate_campaign_request
from app.schemas.campaign_request import CampaignRequest
from app.schemas.enums import CampaignObjective


def _make_request(**overrides) -> CampaignRequest:
    defaults = dict(
        product_name="Acme Widget",
        product_description="A durable widget that helps small teams ship faster.",
        campaign_objective=CampaignObjective.BRAND_AWARENESS,
    )
    defaults.update(overrides)
    return CampaignRequest(**defaults)


def test_valid_request_passes():
    validate_campaign_request(_make_request())  # should not raise


def test_degenerate_description_is_rejected():
    request = _make_request(product_description="aaaaaaaaaaaaaa")
    with pytest.raises(RequestValidationError):
        validate_campaign_request(request)


def test_non_positive_duration_is_rejected_defense_in_depth():
    # Pydantic's `ge=1` constraint already blocks this at the schema level;
    # this test exercises the guardrail's own check directly by
    # constructing the model without validation (model_construct), the way
    # a future caller that skips Pydantic validation still would be caught.
    request = CampaignRequest.model_construct(
        product_name="Acme Widget",
        product_description="A durable widget that helps small teams ship faster.",
        campaign_objective=CampaignObjective.BRAND_AWARENESS,
        campaign_duration_days=0,
    )
    with pytest.raises(RequestValidationError):
        validate_campaign_request(request)
