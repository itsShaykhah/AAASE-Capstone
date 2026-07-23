"""Structured-output validation (mermaid node GR3/GR4).

LLMs are asked to reply with JSON matching a Pydantic schema (see
app/llm/structured_output.py for the prompting side). This module owns the
parsing/validation half: strip incidental markdown fences, parse JSON, and
validate against the target schema, raising one clear exception either way
so the retry layer has something unambiguous to react to.
"""

from __future__ import annotations

import json
import re
from typing import TypeVar

from pydantic import BaseModel, ValidationError

from app.guardrails.exceptions import OutputValidationError

SchemaT = TypeVar("SchemaT", bound=BaseModel)

_CODE_FENCE_PATTERN = re.compile(r"^```(?:json)?\s*|\s*```$", re.MULTILINE)


def strip_code_fences(raw_text: str) -> str:
    """Remove ```json ... ``` fences a model may wrap its JSON reply in."""
    return _CODE_FENCE_PATTERN.sub("", raw_text.strip()).strip()


def parse_structured_output(raw_text: str, schema: type[SchemaT]) -> SchemaT:
    """Parse `raw_text` as JSON and validate it against `schema`.

    Raises OutputValidationError (never a raw JSONDecodeError/ValidationError)
    so callers only need to handle one exception type.
    """
    cleaned = strip_code_fences(raw_text)
    try:
        payload = json.loads(cleaned)
    except json.JSONDecodeError as exc:
        raise OutputValidationError(f"Model output was not valid JSON: {exc}") from exc

    try:
        return schema.model_validate(payload)
    except ValidationError as exc:
        raise OutputValidationError(f"Model output failed schema validation: {exc}") from exc
