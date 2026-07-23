"""Structured-output generation: prompt an LLM for JSON, validate, retry,
and fail over across every configured key and provider before giving up.

This is the one place agents/services go to turn a prompt into a validated
Pydantic object. It deliberately does *not* know about mock mode or
fallback content — that decision belongs to each service, which has the
context (the original request, upstream results) needed to build a good
fallback. This module's job ends at "try every available model, get a
validated schema instance, or raise once everything is exhausted."

Failover strategy
------------------
`LLMFactory.get_chat_model_candidates` returns an ordered list of chat
models (e.g. Groq key 1, key 2, key 3, then OpenRouter key 1, 2, ...). For
each candidate:

- A transport/API failure (auth error, rate limit, timeout) moves to the
  *next candidate immediately* — retrying the same exhausted key wastes
  time and quota that's better spent trying a fresh one.
- A malformed response (bad JSON, schema mismatch) is retried *on the same
  candidate* with a corrective nudge up to `max_retries` times, since
  that's a model-quality issue a nudge can plausibly fix, not a key
  problem. Only after that does it move on to the next candidate.

Only once every candidate has been exhausted does this raise, at which
point the caller falls back to deterministic content.
"""

from __future__ import annotations

import json
from typing import TypeVar

from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.messages import BaseMessage, HumanMessage, SystemMessage
from pydantic import BaseModel

from app.config.settings import LLMConfig
from app.guardrails.exceptions import OutputValidationError
from app.guardrails.output_validation import parse_structured_output
from app.guardrails.retry import retry_with_backoff
from app.llm.exceptions import LLMInvocationError
from app.llm.factory import LLMFactory
from app.schemas.enums import AgentKey

SchemaT = TypeVar("SchemaT", bound=BaseModel)

_RETRY_NUDGE = (
    "Your previous reply could not be parsed as valid JSON matching the required "
    "schema. Reply again with ONLY the corrected JSON object — no prose, no markdown fences."
)


def _build_system_prompt(system_prompt: str, schema: type[BaseModel]) -> str:
    schema_json = json.dumps(schema.model_json_schema(), indent=2)
    return (
        f"{system_prompt}\n\n"
        "Respond with ONLY a single JSON object (no prose, no markdown code fences) "
        f"that matches this JSON schema:\n{schema_json}"
    )


def _invoke_with_format_retries(
    chat_model: BaseChatModel,
    full_system_prompt: str,
    user_prompt: str,
    schema: type[SchemaT],
    max_retries: int,
) -> SchemaT:
    """Call one candidate model, retrying only on malformed-output errors.

    A transport/API exception from `chat_model.invoke` is intentionally
    left to propagate immediately (not retried here) — the caller's
    candidate loop is what decides to move on to the next key/provider.
    """

    def _attempt(attempt_number: int) -> SchemaT:
        messages: list[BaseMessage] = [
            SystemMessage(content=full_system_prompt),
            HumanMessage(content=user_prompt),
        ]
        if attempt_number > 1:
            messages.append(HumanMessage(content=_RETRY_NUDGE))

        response = chat_model.invoke(messages)
        return parse_structured_output(response.content, schema)

    return retry_with_backoff(
        _attempt,
        max_attempts=max_retries + 1,
        retryable_exceptions=(OutputValidationError,),
    )


def generate_structured_response(
    llm_factory: LLMFactory,
    agent_key: AgentKey,
    system_prompt: str,
    user_prompt: str,
    schema: type[SchemaT],
    max_retries: int,
) -> tuple[SchemaT, LLMConfig]:
    """Try every configured key/provider for `agent_key` and return a
    validated `schema` instance from whichever one succeeds first.

    Raises OutputValidationError or LLMInvocationError only once every
    candidate has failed; callers are expected to fall back to
    deterministic content (app/llm/fallback_content.py) rather than let
    the whole run crash.
    """
    candidates = llm_factory.get_chat_model_candidates(agent_key)
    full_system_prompt = _build_system_prompt(system_prompt, schema)

    last_exception: Exception | None = None
    for chat_model, llm_config in candidates:
        try:
            result = _invoke_with_format_retries(chat_model, full_system_prompt, user_prompt, schema, max_retries)
        except OutputValidationError as exc:
            last_exception = exc
            continue
        except Exception as exc:  # noqa: BLE001 - provider SDKs raise many distinct transport error types
            last_exception = LLMInvocationError(f"{llm_config.provider.value}:{llm_config.model} - {exc}")
            continue
        else:
            return result, llm_config

    assert last_exception is not None  # candidates is never empty (factory raises first)
    raise last_exception
