"""Prompt templates, one module per agent.

Prompts live here — not inlined in services — so wording can be tuned by
whoever owns "does the output read well" without touching orchestration or
retry logic. Each module exposes a `build_system_prompt` and one or more
`build_*_user_prompt` functions that return plain strings.
"""
