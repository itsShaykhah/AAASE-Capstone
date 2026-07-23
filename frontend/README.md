# AI Marketing Team — Frontend

A React + Vite + TypeScript dashboard for the AI Marketing Team backend. This app is a **pure HTTP client** of the FastAPI API in `../app` — it never talks to LangGraph, the LLM layer, or search directly, and the backend was intentionally left unmodified when this frontend was built (see the root README's Architecture section).

## Stack

- **React 18 + Vite + TypeScript**
- **Tailwind CSS** + **shadcn/ui** primitives (hand-vendored under `src/components/ui`, not installed via the shadcn CLI)
- **Axios** for the API client (`src/lib/api.ts`)
- **React Router** for the five pages (Dashboard, New Campaign, Campaign Results, Observability, About)
- **Plotly** (`react-plotly.js` via its `/factory` entry + `plotly.js-dist-min`, for a smaller bundle) for charts
- **Lucide React** icons, **sonner** for toasts

## Setup

```bash
npm install
cp .env.example .env.local   # VITE_API_BASE_URL, defaults to http://127.0.0.1:8000
npm run dev
```

Requires the backend running separately (`uvicorn app.api.main:app --reload` from the repo root — see the root README).

## Scripts

| Command | What it does |
|---|---|
| `npm run dev` | Start the Vite dev server (default port 5173) |
| `npm run build` | Type-check (`tsc -b`) then build to `dist/` |
| `npm run preview` | Preview the production build locally |
| `npm run lint` | Run ESLint |

## Structure

```
src/
  lib/            api client, TypeScript types mirroring the backend schemas, chart theme, utils
  context/        CampaignContext (session-only campaign history/state) and ThemeContext (light/dark)
  hooks/          useApiHealth, small hooks
  components/
    ui/           shadcn-style primitives (button, card, tabs, badge, ...)
    layout/       AppShell, Sidebar, TopBar, PageHeader
    campaign/     the New Campaign form + execution progress indicator
    results/      per-tab result renderers (research, strategy, content, QA) + export buttons
    observability/  metrics cards, provider badges, event log table
    charts/       the four Plotly chart wrappers
  pages/          one file per route
```

## Data model

`src/lib/types.ts` hand-mirrors `app/schemas/*.py`. If the backend's schemas change, this is the one file to update on the frontend side — everything else imports types from here, so a mismatch surfaces as a TypeScript error rather than a runtime bug.

## No persistence, by design

There is no database on either side. `CampaignContext` keeps whatever campaigns you've generated in memory for the current browser session (the Dashboard's "recent campaigns" list) — refreshing the page clears it, matching the backend's own no-persistence design.

## A note on "execution progress"

The backend runs all four agents as a single synchronous request (no streaming). The New Campaign page's step checklist is therefore a **time-based estimate**, clearly labeled as such in the UI and in `src/components/campaign/ExecutionProgress.tsx` — not a claim of live per-agent updates. Exact per-agent durations are rendered from the real `observability` data once the response arrives (Observability page).
