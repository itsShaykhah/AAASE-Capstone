"""Business logic for each agent, kept separate from both LangGraph
orchestration (app/graph) and the thin agent wrappers (app/agents).

A service owns: building the prompt inputs, calling the LLM through
`generate_structured_response`, deciding what "graceful degradation" means
for that agent, and any deterministic post-processing. Agents stay thin by
delegating everything here — this is what the project brief means by
"avoid putting all logic inside nodes."
"""
