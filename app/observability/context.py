"""ObservabilityContext: the single facade the rest of the app depends on.

One instance is created per campaign run (by the coordinator) and passed
through the graph state. Nodes/agents call `observe_agent(...)` around their
work; nothing else needs to know that four separate O1-O5 components exist
underneath. This is the seam that would let us swap in Langfuse or OpenTelemetry
later (see resources-from-instrcutor-do-not-modify/04_STRETCH_observability.md)
without touching agents or the graph.
"""

from __future__ import annotations

import time
from contextlib import contextmanager
from typing import Iterator

from app.observability.event_logger import EventLogger
from app.observability.execution_tracer import ExecutionTracer
from app.observability.metrics_collector import MetricsCollector
from app.observability.state_tracer import StateTracer
from app.observability.trace_id import new_trace_id
from app.schemas.enums import AgentKey


class ObservabilityContext:
    """Bundles trace ID, event logging, metrics, execution and state tracing
    for exactly one campaign generation run.
    """

    def __init__(self, trace_id: str | None = None) -> None:
        self.trace_id = trace_id or new_trace_id()
        self.event_logger = EventLogger(self.trace_id)
        self.metrics = MetricsCollector()
        self.execution_tracer = ExecutionTracer()
        self.state_tracer = StateTracer()
        self._run_started_at = time.perf_counter()

    @contextmanager
    def observe_agent(self, agent_key: AgentKey) -> Iterator[dict]:
        """Wrap one agent's execution with logging, timing, and metrics.

        Yields a mutable dict the caller may populate with `provider` (the
        LLM provider actually used) before the block ends, so it can be
        recorded alongside the duration.
        """
        self.event_logger.log("agent_started", agent=agent_key.value)
        agent_context: dict = {}
        try:
            with self.execution_tracer.trace(agent_key.value):
                yield agent_context
        except Exception as exc:
            duration_ms = self.execution_tracer.steps[-1]["duration_ms"]
            self.metrics.record_agent_duration(agent_key.value, duration_ms)
            self.metrics.record_error(f"{agent_key.value}: {exc}")
            self.event_logger.log(
                "agent_failed", agent=agent_key.value, duration_ms=duration_ms, error=str(exc)
            )
            raise
        else:
            duration_ms = self.execution_tracer.steps[-1]["duration_ms"]
            provider = agent_context.get("provider")
            self.metrics.record_agent_duration(agent_key.value, duration_ms)
            if provider:
                self.metrics.record_provider(agent_key.value, provider)
            self.event_logger.log(
                "agent_completed", agent=agent_key.value, duration_ms=duration_ms, provider=provider
            )

    def record_state(self, node_name: str, state: dict) -> None:
        """Snapshot which state keys are populated after a node runs."""
        self.state_tracer.snapshot(node_name, state)

    def total_duration_ms(self) -> float:
        """Wall-clock time since this context (i.e. the run) started."""
        return round((time.perf_counter() - self._run_started_at) * 1000, 2)
