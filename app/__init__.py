"""AI Marketing Team — a LangGraph multi-agent system that turns a product
brief into a complete, ready-to-review marketing campaign.

This package is organized by responsibility rather than by agent, so that
config, prompts, LLM/search access, guardrails, and observability can each
evolve independently of the agents that use them. See app/graph/coordinator.py
for the entrypoint that wires everything together.
"""
