/**
 * Progress indicator shown while POST /api/campaigns is in flight.
 *
 * Important honesty note: the backend runs the four agents as one
 * synchronous request (no SSE/streaming — see app/graph/coordinator.py,
 * which is intentionally not being changed by this frontend rewrite), so
 * there is no real per-step signal to render here. This is a
 * *time-based estimate* of progress through the known pipeline order,
 * clearly labeled as such, not a claim of live per-agent updates. The
 * real, exact per-agent durations are rendered from `observability` once
 * the response actually arrives (see ObservabilityPage).
 */

import { useEffect, useState } from "react";
import { CheckCircle2, Circle, Loader2 } from "lucide-react";

import { Progress } from "@/components/ui/progress";
import { AGENT_LABELS, AGENT_ORDER } from "@/lib/types";

const ESTIMATED_TOTAL_MS = 45_000;

export function ExecutionProgress() {
  const [elapsedMs, setElapsedMs] = useState(0);

  useEffect(() => {
    const startedAt = Date.now();
    const interval = setInterval(() => setElapsedMs(Date.now() - startedAt), 200);
    return () => clearInterval(interval);
  }, []);

  const estimatedPercent = Math.min(96, (elapsedMs / ESTIMATED_TOTAL_MS) * 100);
  const activeIndex = Math.min(
    AGENT_ORDER.length - 1,
    Math.floor((elapsedMs / ESTIMATED_TOTAL_MS) * AGENT_ORDER.length)
  );

  return (
    <div className="space-y-6 rounded-xl border bg-card p-6">
      <div className="flex items-center gap-3">
        <Loader2 className="h-5 w-5 animate-spin text-primary" />
        <div>
          <p className="font-medium">Running the campaign pipeline...</p>
          <p className="text-sm text-muted-foreground">
            Elapsed {(elapsedMs / 1000).toFixed(0)}s — typically takes 20-90s depending on provider
            response times.
          </p>
        </div>
      </div>

      <Progress value={estimatedPercent} />

      <ol className="space-y-3">
        {AGENT_ORDER.map((key, index) => {
          const isDone = index < activeIndex;
          const isActive = index === activeIndex;
          return (
            <li key={key} className="flex items-center gap-3 text-sm">
              {isDone ? (
                <CheckCircle2 className="h-4 w-4 text-success" />
              ) : isActive ? (
                <Loader2 className="h-4 w-4 animate-spin text-primary" />
              ) : (
                <Circle className="h-4 w-4 text-muted-foreground" />
              )}
              <span className={isDone || isActive ? "text-foreground" : "text-muted-foreground"}>
                {AGENT_LABELS[key]}
              </span>
            </li>
          );
        })}
      </ol>

      <p className="text-xs text-muted-foreground">
        This checklist is a time-based estimate, not a live signal — the API call resolves once, and
        exact per-agent durations appear on the Observability page after it completes.
      </p>
    </div>
  );
}
