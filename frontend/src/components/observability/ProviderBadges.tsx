import { Badge } from "@/components/ui/badge";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { AGENT_LABELS, AGENT_ORDER, type AgentKey } from "@/lib/types";

function badgeVariantFor(provider: string): "secondary" | "warning" | "outline" {
  if (provider === "fallback") return "warning";
  if (provider === "mock") return "outline";
  return "secondary";
}

export function ProviderBadges({ providerUsed }: { providerUsed: Record<string, string> }) {
  const entries = AGENT_ORDER.filter((key) => key in providerUsed);

  if (entries.length === 0) {
    return null;
  }

  return (
    <Card>
      <CardHeader>
        <CardTitle className="text-base">Provider used per agent</CardTitle>
      </CardHeader>
      <CardContent className="flex flex-wrap gap-3">
        {entries.map((key) => {
          const provider = providerUsed[key];
          return (
            <div key={key} className="flex items-center gap-2 rounded-lg border px-3 py-2">
              <span className="text-sm font-medium">{AGENT_LABELS[key as AgentKey]}</span>
              <Badge variant={badgeVariantFor(provider)}>{provider}</Badge>
            </div>
          );
        })}
      </CardContent>
    </Card>
  );
}
