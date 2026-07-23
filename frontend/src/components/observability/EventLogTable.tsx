import { useMemo, useState } from "react";
import { Search } from "lucide-react";

import { Badge } from "@/components/ui/badge";
import { Input } from "@/components/ui/input";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table";
import type { ObservabilityEvent } from "@/lib/types";

const EVENT_BADGE_VARIANT: Record<string, "secondary" | "success" | "warning" | "destructive"> = {
  agent_started: "secondary",
  agent_completed: "success",
  agent_degraded: "warning",
  agent_failed: "destructive",
  agent_unhandled_error: "destructive",
  search_unavailable: "warning",
  search_provider_failed: "warning",
  run_failed: "destructive",
};

function eventDetail(event: ObservabilityEvent): string {
  if (event.reason) return event.reason;
  if (event.error) return event.error;
  if (event.query) return `query: "${event.query}"`;
  if (event.provider) return `provider: ${event.provider}`;
  return "";
}

export function EventLogTable({ events }: { events: ObservabilityEvent[] }) {
  const [search, setSearch] = useState("");

  const filtered = useMemo(() => {
    if (!search.trim()) return events;
    const needle = search.toLowerCase();
    return events.filter((event) =>
      JSON.stringify(event).toLowerCase().includes(needle)
    );
  }, [events, search]);

  return (
    <div className="space-y-3">
      <div className="relative max-w-sm">
        <Search className="absolute left-2.5 top-2.5 h-4 w-4 text-muted-foreground" />
        <Input
          placeholder="Filter events..."
          value={search}
          onChange={(event) => setSearch(event.target.value)}
          className="pl-8"
        />
      </div>

      <div className="rounded-lg border">
        <Table>
          <TableHeader>
            <TableRow>
              <TableHead>Time</TableHead>
              <TableHead>Event</TableHead>
              <TableHead>Agent</TableHead>
              <TableHead>Duration</TableHead>
              <TableHead>Detail</TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            {filtered.map((event, index) => (
              <TableRow key={`${event.timestamp}-${index}`}>
                <TableCell className="whitespace-nowrap font-mono text-xs text-muted-foreground">
                  {new Date(event.timestamp).toLocaleTimeString()}
                </TableCell>
                <TableCell>
                  <Badge variant={EVENT_BADGE_VARIANT[event.event] ?? "secondary"}>{event.event}</Badge>
                </TableCell>
                <TableCell className="text-sm">{event.agent ?? "—"}</TableCell>
                <TableCell className="text-sm">
                  {event.duration_ms !== undefined ? `${Math.round(event.duration_ms)}ms` : "—"}
                </TableCell>
                <TableCell className="max-w-md truncate text-sm text-muted-foreground" title={eventDetail(event)}>
                  {eventDetail(event) || "—"}
                </TableCell>
              </TableRow>
            ))}
            {filtered.length === 0 && (
              <TableRow>
                <TableCell colSpan={5} className="py-6 text-center text-sm text-muted-foreground">
                  No events match "{search}".
                </TableCell>
              </TableRow>
            )}
          </TableBody>
        </Table>
      </div>
    </div>
  );
}
