"""Lightweight in-memory metrics (mermaid node O3 — Metrics Collector).

Deliberately not a Prometheus/StatsD client: for a single-request pipeline
run, an in-memory rollup that gets returned to the caller is simpler to
reason about and enough to satisfy the "execution duration / provider used
/ errors" observability requirement. Swapping this for a real metrics
backend later only touches this one file.
"""

from __future__ import annotations


class MetricsCollector:
    """Accumulates per-agent timing, provider usage, and errors for one run."""

    def __init__(self) -> None:
        self._agent_durations_ms: dict[str, float] = {}
        self._provider_used: dict[str, str] = {}
        self._errors: list[str] = []

    def record_agent_duration(self, agent_key: str, duration_ms: float) -> None:
        self._agent_durations_ms[agent_key] = duration_ms

    def record_provider(self, agent_key: str, provider: str) -> None:
        self._provider_used[agent_key] = provider

    def record_error(self, message: str) -> None:
        self._errors.append(message)

    @property
    def agent_durations_ms(self) -> dict[str, float]:
        return dict(self._agent_durations_ms)

    @property
    def provider_used(self) -> dict[str, str]:
        return dict(self._provider_used)

    @property
    def errors(self) -> list[str]:
        return list(self._errors)
