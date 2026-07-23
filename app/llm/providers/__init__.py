"""Concrete LLM provider adapters, one module per provider.

Each adapter implements `BaseLLMProvider.build_chat_model` and owns exactly
the provider-specific wiring (SDK class, base URL, headers). Adding a new
provider means adding one file here plus one branch in
`app.llm.factory.LLMFactory._build_provider` — no other module changes.
"""
