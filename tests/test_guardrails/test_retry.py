from __future__ import annotations

import pytest

from app.guardrails.retry import retry_with_backoff


def test_retry_returns_result_once_operation_succeeds():
    attempts: list[int] = []

    def flaky(attempt_number: int) -> str:
        attempts.append(attempt_number)
        if attempt_number < 3:
            raise ValueError("not yet")
        return "ok"

    result = retry_with_backoff(
        flaky, max_attempts=5, base_delay_seconds=0, retryable_exceptions=(ValueError,)
    )

    assert result == "ok"
    assert attempts == [1, 2, 3]


def test_retry_raises_after_exhausting_max_attempts():
    def always_fails(attempt_number: int) -> str:
        raise ValueError(f"attempt {attempt_number} failed")

    with pytest.raises(ValueError):
        retry_with_backoff(
            always_fails, max_attempts=2, base_delay_seconds=0, retryable_exceptions=(ValueError,)
        )


def test_retry_does_not_catch_non_retryable_exceptions():
    def raises_type_error(attempt_number: int) -> str:
        raise TypeError("unexpected")

    with pytest.raises(TypeError):
        retry_with_backoff(
            raises_type_error, max_attempts=3, base_delay_seconds=0, retryable_exceptions=(ValueError,)
        )
