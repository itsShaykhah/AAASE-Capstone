## Acknowledgements

This project was developed as part of the **Advanced Engineering Agentic AI Systems** program offered by **SDAIA Academy**.

Organization:
https://github.com/SDAIAAcademy
---

# AI Marketing Team

A LangGraph-based multi-agent system that turns a product brief into a complete, ready-to-review marketing campaign — market research, strategy, platform-specific content, and a quality-assurance pass — displayed in a modern React dashboard.

> **Team:** _add your name(s) and GitHub username(s) here, with one line on each person's contribution._

## Problem statement

Producing a first-draft marketing campaign (research, strategy, and copy for five+ channels) is a repetitive, multi-step process that a small team or solo founder redoes for every product launch. This project automates that first draft: given a short product brief, it researches the market, drafts a channel strategy, writes the actual platform copy, and runs a QA pass — so a human starts from a reviewed draft instead of a blank page.

**This system does not publish anything.** It generates a complete campaign package for a human to review, edit, and export before publishing through their own tools.

## How the agent solves it

```
Product brief
   -> Request validation + guardrails (prompt-injection check, field checks)
   -> Market Intelligence Agent   (web search -> audience/competitors/trends)
   -> Campaign Strategy Agent     (goal, channels, calendar, budget split)
   -> Content Generation Agent    (Instagram/X/LinkedIn/Email/Ads/Hashtags/CTA)
   -> Quality Assurance Agent     (LLM review + deterministic fixes + approval)
   -> Generated deliverables (rendered in the UI, exportable as Markdown/PDF)
```

**The agentic behavior** is a **multi-role LangGraph pipeline with tool use**: a `StateGraph` routes a shared state object through four specialized agents in sequence; the Market Intelligence agent calls a real web-search tool (Tavily, falling back to Serper) as part of its reasoning; and the Quality Assurance agent evaluates the Content Generation agent's output against explicit checks before final approval.

## Architecture

Full diagram: [`mermaid-files/architecture.md`](mermaid-files/architecture.md).

```
User -> React SPA -> FastAPI Gateway -> Request Validation -> Guardrail Manager
      -> LangGraph Coordinator
      -> Market Intelligence Agent -> Campaign Strategy Agent
      -> Content Generation Agent -> Quality Assurance Agent
      -> Generated Deliverables (+ Markdown/PDF export)
```

Cross-cutting layers used by every agent:

- **LLM Factory** (`app/llm`) — routes each agent's calls to Groq or OpenRouter based on configuration; no agent ever imports a provider SDK directly.
- **Search Service** (`app/search`) — Tavily primary, Serper fallback; used only by Market Intelligence.
- **Guardrails** (`app/guardrails`) — request validation, prompt-injection detection, structured-output validation, retry/backoff.
- **Observability** (`app/observability`) — trace IDs, structured event logs, per-agent metrics, execution/state tracing, surfaced in the UI's Observability panel.

## Tech stack

| Layer | Choice | Why |
|---|---|---|
| Agent framework | [LangGraph](https://docs.langchain.com/oss/python/langgraph) | Explicit `StateGraph` makes a deterministic multi-agent pipeline easy to read, test, and extend. |
| LLM providers | Groq, OpenRouter (via `langchain-groq` / `langchain-openai`) | Both have usable free tiers; abstracted behind one factory so switching is a config change. |
| Search | Tavily (primary), Serper (fallback) | Tavily is built for LLM consumption; Serper is a reliable, cheap fallback. |
| Backend | FastAPI | Async-ready, typed, self-documenting (`/docs`), easy to deploy on Render. |
| Frontend | React + Vite + TypeScript, Tailwind CSS, shadcn/ui, Plotly | A dashboard-style SPA that is a pure HTTP client of the FastAPI backend (Axios) — deployable independently on Netlify. |
| Data contracts | Pydantic v2 (backend) / hand-mirrored TypeScript types (frontend) | Every agent boundary is a validated schema, which is also what makes structured-output validation possible. |
| Export | fpdf2 | Pure-Python PDF generation, no system dependencies (works on Render's free tier). |

## Project structure

```
app/
  config/        typed Settings (env-var driven — see .env.example)
  schemas/        Pydantic/TypedDict data contracts shared across the system
  llm/            LLM Factory + provider adapters + structured-output helper
  search/         SearchService (Tavily -> Serper fallback)
  guardrails/     request validation, prompt-injection detection, retry, output validation
  observability/  trace IDs, event logging, metrics, execution/state tracing
  prompts/        prompt templates, one module per agent
  services/       business logic per agent (what each agent actually does)
  agents/         thin LangGraph-facing adapters around each service
  graph/          the LangGraph StateGraph itself (nodes + coordinator)
  api/            FastAPI app, routes, dependency wiring
tests/            mirrors app/ — guardrails, agents, services, graph, utils
frontend/         React + Vite + TypeScript SPA (pure HTTP client of the API — see frontend/README section below)
```

## How to run

**Backend (API):**

```bash
git clone <repo-url> && cd AAASE-CAPSTONE
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env             # then add your API keys (or set MOCK_MODE=true)

uvicorn app.api.main:app --reload
```

The API is now at `http://127.0.0.1:8000` (interactive docs at `/docs`).

**No API keys yet?** Set `MOCK_MODE=true` in `.env` — the whole pipeline runs on deterministic fixture content so you can see the full UI and pipeline flow with zero external calls.

**Frontend (React SPA), in a second terminal:**

```bash
cd frontend
npm install
cp .env.example .env.local       # defaults to http://127.0.0.1:8000, adjust if needed
npm run dev
```

Open the URL Vite prints (usually http://localhost:5173).

### Running tests

```bash
pytest
```

All tests run fully offline (mock mode / stubbed services) — no API keys required.

## Demonstration evidence

_Add screenshots or a short recording here, e.g._
```markdown
![Campaign form](docs/images/form.png)
![Generated campaign](docs/images/results.png)
![Observability panel](docs/images/observability.png)
```

## Deployment

- **Backend:** [Render](https://render.com), one free-tier web service (see `render.yaml`) running `ai-marketing-api`.
- **Frontend:** [Netlify](https://netlify.com), building `frontend/` (see `frontend/netlify.toml`). Set the `VITE_API_BASE_URL` environment variable in Netlify's site settings to the deployed Render API URL, then set the API's `CORS_ALLOW_ORIGINS` env var to that Netlify URL (defaults to `*`, which works but is looser than necessary once you know the real origin).

The two deploy and redeploy independently — the frontend is a pure HTTP client of the API's stable contract (`POST /api/campaigns`, `POST /api/campaigns/export/{markdown,pdf}`, `GET /health`).

## Limitations & future work

- The Quality Assurance agent reviews and can approve/flag content, but the pipeline is linear (no automatic revision loop back to Content Generation) — matching the fixed architecture diagram for v1.
- No persistence: campaigns exist only for the session that generated them (by design for v1 — see the architecture notes).
- Prompt-injection detection is regex/heuristic, not model-based; a paraphrased attack can still slip through.
- Search quality depends on the free-tier rate limits of Tavily/Serper.
- The frontend's per-agent execution progress (New Campaign page) is a time-based estimate, not a live stream — the backend returns one response after the full pipeline finishes; exact per-agent durations appear on the Observability page once it does.
- Next steps: a revision loop gated on the QA agent's `overall_approved` flag, per-user campaign history (would need a database), and server-sent events for real per-agent progress.
