"""LLM provider abstraction.

Nothing outside this package should import `langchain_groq` or
`langchain_openai` directly — agents and services depend on
`LLMFactory` and `generate_structured_response` only. That's what makes
"switch provider/model via configuration" a real property of the system
rather than an aspiration: there is exactly one place that constructs a
chat model.
"""

from app.llm.factory import LLMFactory
from app.llm.structured_output import generate_structured_response

__all__ = ["LLMFactory", "generate_structured_response"]
