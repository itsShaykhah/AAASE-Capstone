"""Agents: the LangGraph-facing adapters for each pipeline stage.

An agent's job is narrow and consistent across all four: read what it
needs out of `CampaignGraphState`, call its Service to do the actual work,
and return a partial state update. Agents know the shape of the graph
state; services don't. That split means:

- Services stay reusable outside LangGraph (unit tests, a future CLI,
  a different orchestrator) since they take plain domain objects in and
  out.
- Swapping the orchestration layer only means rewriting agents, not
  services.
- graph/nodes.py stays a one-line-per-node wrapper around `agent.run`.

Each agent also acts as a last line of defense: if its Service raises an
exception nobody anticipated (a real bug, not a handled LLM/search
failure), the agent catches it, records it in `errors`, and substitutes
deterministic fallback content so one stage's bug doesn't crash the whole
campaign run.
"""
