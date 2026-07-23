from __future__ import annotations

import pytest
from pydantic import BaseModel

from app.guardrails.exceptions import OutputValidationError
from app.guardrails.output_validation import parse_structured_output, strip_code_fences


class _Sample(BaseModel):
    name: str
    score: int


def test_strip_code_fences_removes_markdown_wrapper():
    raw = '```json\n{"name": "a", "score": 1}\n```'
    assert strip_code_fences(raw) == '{"name": "a", "score": 1}'


def test_parse_structured_output_accepts_valid_json():
    result = parse_structured_output('{"name": "widget", "score": 5}', _Sample)
    assert result == _Sample(name="widget", score=5)


def test_parse_structured_output_rejects_invalid_json():
    with pytest.raises(OutputValidationError):
        parse_structured_output("not json at all", _Sample)


def test_parse_structured_output_rejects_schema_mismatch():
    with pytest.raises(OutputValidationError):
        parse_structured_output('{"name": "widget"}', _Sample)
