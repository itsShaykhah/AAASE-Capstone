import { Activity } from "lucide-react";
import { NavLink } from "react-router-dom";

import { AgentDurationChart } from "@/components/charts/AgentDurationChart";
import { PageHeader } from "@/components/layout/PageHeader";
import { EventLogTable } from "@/components/observability/EventLogTable";
import { MetricsCards } from "@/components/observability/MetricsCards";
import { ProviderBadges } from "@/components/observability/ProviderBadges";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { useCampaign } from "@/context/CampaignContext";

export function ObservabilityPage() {
  const { currentCampaign } = useCampaign();

  if (!currentCampaign) {
    return (
      <div>
        <PageHeader title="Observability" />
        <div className="flex flex-col items-center justify-center gap-4 rounded-xl border border-dashed py-24 text-center">
          <Activity className="h-10 w-10 text-muted-foreground" />
          <div>
            <p className="font-medium">Nothing to observe yet</p>
            <p className="text-sm text-muted-foreground">
              Generate a campaign to see trace IDs, timing, and the event log.
            </p>
          </div>
          <Button asChild>
            <NavLink to="/new-campaign">Create a campaign</NavLink>
          </Button>
        </div>
      </div>
    );
  }

  const { observability } = currentCampaign;

  return (
    <div className="space-y-4">
      <PageHeader
        title="Observability"
        description={`Trace, timing, and event log for "${currentCampaign.request.product_name}"`}
      />

      <MetricsCards summary={observability} />

      <div className="grid gap-4 lg:grid-cols-2">
        <Card>
          <CardHeader>
            <CardTitle className="text-base">Execution duration per agent</CardTitle>
          </CardHeader>
          <CardContent>
            <AgentDurationChart agentDurationsMs={observability.agent_durations_ms} />
          </CardContent>
        </Card>

        <ProviderBadges providerUsed={observability.provider_used} />
      </div>

      <Card>
        <CardHeader>
          <CardTitle className="text-base">Event log</CardTitle>
        </CardHeader>
        <CardContent>
          <EventLogTable events={observability.events} />
        </CardContent>
      </Card>
    </div>
  );
}
