"""LangGraph orchestration.

This package contains only wiring: node functions (nodes.py) that adapt
agents to LangGraph's node signature, and the coordinator (coordinator.py)
that builds the StateGraph, compiles it, and runs one campaign end to end.
No business logic lives here — see app/agents and app/services for that —
which is what keeps the graph itself easy to read as a one-page picture of
the pipeline.
"""

from app.graph.coordinator import CampaignCoordinator

__all__ = ["CampaignCoordinator"]
