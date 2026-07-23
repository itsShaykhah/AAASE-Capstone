import { Bot, GitBranch, Layers, Search, ShieldCheck } from "lucide-react";

import { PageHeader } from "@/components/layout/PageHeader";
import { Badge } from "@/components/ui/badge";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";

const PIPELINE_STEPS = [
  {
    icon: Search,
    title: "Market Intelligence Agent",
    description:
      "Generates search queries, calls Tavily (falling back to Serper), and synthesizes audience, competitors, and trends.",
  },
  {
    icon: Layers,
    title: "Campaign Strategy Agent",
    description: "Turns research into a goal, channel mix, content calendar, and budget allocation.",
  },
  {
    icon: Bot,
    title: "Content Generation Agent",
    description:
      "Writes the full platform-specific content package in one consistent brand voice — for review, not auto-publishing.",
  },
  {
    icon: ShieldCheck,
    title: "Quality Assurance Agent",
    description:
      "Reviews brand consistency, tone, and grammar, applies deterministic formatting fixes, and issues final approval.",
  },
];

const TECH_STACK = [
  "LangGraph",
  "FastAPI",
  "Groq",
  "OpenRouter",
  "Tavily",
  "Serper",
  "Pydantic",
  "React",
  "Vite",
  "Tailwind CSS",
  "Plotly",
];

export function AboutPage() {
  return (
    <div className="space-y-6">
      <PageHeader
        title="About"
        description="AI Marketing Team — a LangGraph multi-agent system that drafts a complete marketing campaign from a product brief."
      />

      <Card>
        <CardHeader>
          <CardTitle className="text-base">What this is</CardTitle>
        </CardHeader>
        <CardContent className="space-y-3 text-sm leading-relaxed text-muted-foreground">
          <p>
            Producing a first-draft marketing campaign — research, strategy, and copy for five-plus
            channels — is a repetitive, multi-step process. This system automates that first draft: given
            a short product brief, it researches the market, drafts a channel strategy, writes platform
            copy, and runs a QA pass, so a human starts from a reviewed draft instead of a blank page.
          </p>
          <p className="font-medium text-foreground">
            It does not publish anything. Every asset is generated for a human to review, edit, and export
            before publishing through their own tools.
          </p>
        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle className="text-base">Pipeline</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="grid gap-4 sm:grid-cols-2">
            {PIPELINE_STEPS.map((step, index) => (
              <div key={step.title} className="flex gap-3 rounded-lg border p-4">
                <div className="flex h-9 w-9 shrink-0 items-center justify-center rounded-lg bg-primary/10 text-primary">
                  <step.icon className="h-4 w-4" />
                </div>
                <div>
                  <p className="text-sm font-medium">
                    {index + 1}. {step.title}
                  </p>
                  <p className="mt-1 text-sm text-muted-foreground">{step.description}</p>
                </div>
              </div>
            ))}
          </div>
        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2 text-base">
            <GitBranch className="h-4 w-4" /> Architecture
          </CardTitle>
        </CardHeader>
        <CardContent className="space-y-2 text-sm text-muted-foreground">
          <p>
            A LangGraph <code className="rounded bg-muted px-1 py-0.5 text-xs">StateGraph</code> routes a
            shared state object through the four agents above in a fixed sequence. Request validation and
            guardrails (prompt-injection detection, structured-output validation, multi-key/provider
            failover, deterministic fallback content) run before and around each step. This React
            application is a pure HTTP client of that FastAPI backend — the frontend can be redeployed or
            replaced independently of the agents, LLM layer, or orchestration.
          </p>
        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle className="text-base">Tech stack</CardTitle>
        </CardHeader>
        <CardContent className="flex flex-wrap gap-2">
          {TECH_STACK.map((tech) => (
            <Badge key={tech} variant="secondary">
              {tech}
            </Badge>
          ))}
        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle className="text-base">Limitations</CardTitle>
        </CardHeader>
        <CardContent className="space-y-2 text-sm text-muted-foreground">
          <p>
            No persistence — campaigns exist only for the browser session that generated them. Prompt-
            injection detection is regex/heuristic, not model-based. Search quality depends on the
            free-tier rate limits of Tavily/Serper, and LLM output depends on the configured providers'
            availability (with automatic key/provider failover before falling back to deterministic
            content).
          </p>
        </CardContent>
      </Card>
    </div>
  );
}
