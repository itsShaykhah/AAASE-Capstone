import { AlertTriangle, Clock, Cpu, Hash } from "lucide-react";
import type { ReactNode } from "react";

import { Card, CardContent } from "@/components/ui/card";
import { CopyButton } from "@/components/ui/copy-button";
import { formatDuration } from "@/lib/utils";
import type { ObservabilitySummary } from "@/lib/types";

interface StatTileProps {
  label: string;
  value: ReactNode;
  icon: ReactNode;
  tone?: "default" | "warning";
}

function StatTile({ label, value, icon, tone = "default" }: StatTileProps) {
  return (
    <Card>
      <CardContent className="flex items-center gap-4 p-4">
        <div
          className={`flex h-10 w-10 shrink-0 items-center justify-center rounded-lg ${
            tone === "warning" ? "bg-warning/15 text-warning" : "bg-primary/10 text-primary"
          }`}
        >
          {icon}
        </div>
        <div className="min-w-0">
          <p className="text-xs text-muted-foreground">{label}</p>
          <div className="truncate text-lg font-semibold">{value}</div>
        </div>
      </CardContent>
    </Card>
  );
}

export function MetricsCards({ summary }: { summary: ObservabilitySummary }) {
  const uniqueProviders = new Set(Object.values(summary.provider_used)).size;

  return (
    <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
      <StatTile
        label="Total duration"
        value={formatDuration(summary.total_duration_ms)}
        icon={<Clock className="h-5 w-5" />}
      />
      <StatTile
        label="Agents executed"
        value={Object.keys(summary.agent_durations_ms).length}
        icon={<Cpu className="h-5 w-5" />}
      />
      <StatTile
        label="Errors / degradations"
        value={summary.errors.length}
        icon={<AlertTriangle className="h-5 w-5" />}
        tone={summary.errors.length > 0 ? "warning" : "default"}
      />
      <StatTile
        label="Providers used"
        value={uniqueProviders || "—"}
        icon={<Hash className="h-5 w-5" />}
      />

      <Card className="sm:col-span-2 lg:col-span-4">
        <CardContent className="flex items-center justify-between gap-4 p-4">
          <div className="min-w-0">
            <p className="text-xs text-muted-foreground">Trace ID</p>
            <p className="truncate font-mono text-sm">{summary.trace_id}</p>
          </div>
          <CopyButton value={summary.trace_id} label="Copy trace ID" />
        </CardContent>
      </Card>
    </div>
  );
}
