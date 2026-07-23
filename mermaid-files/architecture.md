# AI Marketing Team - Multi-Agent Architecture

```mermaid
flowchart TD

%% ============================
%% CLIENT
%% ============================

START([User])

START --> UI[React Frontend / Streamlit UI]

UI --> API

%% ============================
%% BACKEND
%% ============================

subgraph BACKEND [Render Backend - FastAPI]

API[FastAPI Gateway]

API --> G1[Request Validation]

G1 --> G2[Guardrail Manager]

G2 --> G3[Coordinator<br/>LangGraph StateGraph]

end

%% ============================
%% LANGGRAPH
%% ============================

subgraph GRAPH [LangGraph Multi-Agent Workflow]

G3 --> A1

A1[Market Intelligence Agent]

A1 --> A2

A2[Campaign Strategy Agent]

A2 --> A3

A3[Content Generation Agent]

A3 --> A4

A4[Quality Assurance Agent]

end

%% ============================
%% AGENT 1
%% ============================

subgraph AGENT1 [Market Intelligence Agent]

M1[Receive Product Brief]

M1 --> M2[Generate Optimized Search Queries]

M2 --> M3[Tavily Search]

M3 --> M4[Serper Fallback]

M4 --> M5[Analyze Search Results]

M5 --> M6[Identify Target Audience]

M6 --> M7[Identify Competitors]

M7 --> M8[Identify Market Trends]

M8 --> M9[Research Summary]

end

A1 -.internal.-> M1

%% ============================
%% AGENT 2
%% ============================

subgraph AGENT2 [Campaign Strategy Agent]

S1[Receive Research Summary]

S1 --> S2[Define Campaign Goal]

S2 --> S3[Select Marketing Channels]

S3 --> S4[Build Content Calendar]

S4 --> S5[Define Content Themes]

S5 --> S6[Allocate Budget]

S6 --> S7[Campaign Strategy]

end

A2 -.internal.-> S1

%% ============================
%% AGENT 3
%% ============================

subgraph AGENT3 [Content Generation Agent]

C1[Receive Campaign Strategy]

C1 --> C2[Generate Brand Voice]

C2 --> C3[Instagram Caption]

C3 --> C4[X Post]

C4 --> C5[LinkedIn Post]

C5 --> C6[Email Campaign]

C6 --> C7[Ad Headlines]

C7 --> C8[Hashtags]

C8 --> C9[Call-To-Action]

C9 --> C10[Content Packaging]

C10 --> C11[Marketing Content]

end

A3 -.internal.-> C1

%% ============================
%% AGENT 4
%% ============================

subgraph AGENT4 [Quality Assurance Agent]

Q1[Receive All Outputs]

Q1 --> Q2[Brand Consistency]

Q2 --> Q3[Tone Validation]

Q3 --> Q4[Grammar Review]

Q4 --> Q5[Marketing Quality Review]

Q5 --> Q6[Guardrail Validation]

Q6 --> Q7[Final Campaign Approval]

end

A4 -.internal.-> Q1

%% ============================
%% OUTPUT
%% ============================

A4 --> OUTPUT

subgraph RESULTS [Generated Deliverables]

R1[Market Research Report]

R2[Campaign Strategy]

R3[Marketing Content Package]

R4[Final Approved Campaign]

R5[Export PDF / Markdown]

end

OUTPUT --> RESULTS

%% ============================
%% LLM LAYER
%% ============================

subgraph LLM [LLM Provider Layer]

L1[LLM Factory / Model Manager]

L2[Groq Provider]

L3[OpenRouter Provider]

end

L1 --> L2

L1 --> L3

%% ============================
%% EXTERNAL SERVICES
%% ============================

subgraph SERVICES [External Services]

E1[Tavily Search API]

E2[Serper Search API]

end

M3 --> E1

M4 --> E2

M9 --> L1

S7 --> L1

C11 --> L1

Q7 --> L1

%% ============================
%% OBSERVABILITY
%% ============================

subgraph OBS [Observability Layer]

O1[Event Logger]

O2[Execution Tracer]

O3[Metrics Collector]

O4[State Tracer]

O5[Trace ID Manager]

end

G3 -.observe.-> O1

A1 -.logs.-> O1

A2 -.logs.-> O1

A3 -.logs.-> O1

A4 -.logs.-> O1

G3 -.trace.-> O2

G3 -.metrics.-> O3

G3 -.state.-> O4

O1 --> O5

%% ============================
%% GUARDRAILS
%% ============================

subgraph SAFE [Guardrail Layer]

GR1[Request Validation]

GR2[Prompt Injection Detection]

GR3[Pydantic Schema Validation]

GR4[Output Validation]

GR5[Retry & Recovery]

end

G2 --> GR1

GR1 --> GR2

GR2 --> GR3

GR3 --> GR4

GR4 --> GR5
```

## Architecture Notes

### Current Scope (Version 1)

This architecture focuses on delivering an end-to-end AI Marketing Team capable of transforming a user's marketing brief into a complete campaign using a coordinated multi-agent workflow. The project prioritizes modularity, explainability, and production-inspired software engineering practices while remaining deployable using free-tier AI services.

### Content Generation

The Content Generation Agent **does not publish content directly** to social media platforms.

Instead, it generates a complete marketing package that is displayed within the application interface, including:

- Instagram caption
- X (Twitter) post
- LinkedIn post
- Email campaign copy
- Advertisement headlines
- Hashtags
- Call-to-action

This simulated approach allows users to review, edit, and export the generated campaign before publishing through their preferred marketing tools.

### Multi-Agent Coordination

The LangGraph Coordinator orchestrates the entire workflow using deterministic routing:

1. Market Intelligence Agent performs market research and audience analysis.
2. Campaign Strategy Agent transforms research into a marketing strategy.
3. Content Generation Agent creates platform-specific marketing assets.
4. Quality Assurance Agent validates consistency, quality, and completeness before returning the final campaign.

Each agent has a single responsibility, making the system modular and easy to extend.

### LLM Provider Abstraction

Rather than coupling agents directly to a specific model, all LLM interactions are routed through a centralized **LLM Factory / Model Manager**.

This abstraction provides:

- Provider independence (Groq or OpenRouter)
- Centralized model configuration
- Simplified provider switching
- Cleaner separation between business logic and LLM implementation

Specific model selection is intentionally configurable and not hardcoded within the architecture.

### Search Layer

Only the **Market Intelligence Agent** performs external web searches.

The remaining agents operate exclusively on structured outputs produced by previous agents, reducing API usage, improving consistency, and minimizing token consumption.

### Guardrails

Guardrails are applied before and after agent execution to improve reliability.

Current safeguards include:

- Request validation
- Prompt injection detection
- Structured output validation using Pydantic
- Output validation
- Retry and graceful recovery mechanisms

### Observability

The pipeline includes lightweight observability to improve transparency and debugging.

Execution metadata includes:

- Agent execution timeline
- Event logging
- State transitions
- Performance metrics
- Trace identifiers

These components make it easier to understand what each agent executed, how long each step required, and where failures occurred during pipeline execution.

### Deployment

The system is designed to be cloud deployable without requiring model hosting or training.

- **Frontend:** React (or Streamlit during development)
- **Backend:** FastAPI hosted on Render
- **Multi-Agent Framework:** LangGraph
- **LLM Providers:** Groq and OpenRouter
- **Search Providers:** Tavily and Serper

All intelligence is provided through external APIs, allowing the application to run entirely on commodity cloud infrastructure.