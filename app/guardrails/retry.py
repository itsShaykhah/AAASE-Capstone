"""Retry with backoff (mermaid node GR5 — Retry & Recovery).

A small, generic helper rather than a dependency like `tenacity` — the
retry policy this project needs (a handful of attempts, linear backoff, a
callback for logging) is simple enough that a dedicated library would add
more surface area than it saves.
"""

from __future__ import annotations

import time
from typing import Callable, TypeVar

ResultT = TypeVar("ResultT")


def retry_with_backoff(
    operation: Callable[[int], ResultT],
    *,
    max_attempts: int,
    base_delay_seconds: float = 1.0,
    retryable_exceptions: tuple[type[Exception], ...] = (Exception,),
    on_retry: Callable[[int, Exception], None] | None = None,
) -> ResultT:
    """Call `operation(attempt_number)` up to `max_attempts` times.

    Retries only on `retryable_exceptions`; anything else propagates
    immediately. Delay grows linearly with the attempt number, which is
    plenty for the free-tier LLM/search rate limits this project targets.
    """
    last_exception: Exception | None = None
    for attempt in range(1, max_attempts + 1):
        try:
            return operation(attempt)
        except retryable_exceptions as exc:
            last_exception = exc
            if on_retry:
                on_retry(attempt, exc)
            if attempt < max_attempts:
                time.sleep(base_delay_seconds * attempt)
    assert last_exception is not None
    raise last_exception
