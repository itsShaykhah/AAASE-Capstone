"""LangGraph node factory.

Every node in this graph has the same shape: call the corresponding
agent's `run(state)`, record a state snapshot for observability, and return
the partial state update for LangGraph to merge. That uniformity means one
factory function serves all four nodes instead of four near-identical
copies.
"""

from __future__ import annotations

from typing import Callable, Protocol

from app.schemas.graph_state import CampaignGraphState


class _RunnableAgent(Protocol):
    def run(self, state: CampaignGraphState) -> dict: ...


def make_node(node_name: str, agent: _RunnableAgent) -> Callable[[CampaignGraphState], dict]:
    """Build a LangGraph node function that delegates to `agent`."""

    def _node(state: CampaignGraphState) -> dict:
        update = agent.run(state)
        state["observability"].record_state(node_name, {**state, **update})
        return update

    _node.__name__ = f"{node_name}_node"
    return _node
