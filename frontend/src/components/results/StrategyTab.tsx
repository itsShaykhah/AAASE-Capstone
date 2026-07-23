import { BudgetAllocationChart } from "@/components/charts/BudgetAllocationChart";
import { CampaignTimelineChart } from "@/components/charts/CampaignTimelineChart";
import { ChannelDistributionChart } from "@/components/charts/ChannelDistributionChart";
import { Badge } from "@/components/ui/badge";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import type { CampaignStrategy } from "@/lib/types";

export function StrategyTab({ strategy }: { strategy: CampaignStrategy | null | undefined }) {
  if (!strategy) {
    return <p className="text-sm text-muted-foreground">No campaign strategy was produced for this run.</p>;
  }

  return (
    <div className="space-y-4">
      <Card>
        <CardHeader>
          <CardTitle className="text-base">Goal & channels</CardTitle>
        </CardHeader>
        <CardContent className="space-y-3">
          <p className="text-sm">{strategy.campaign_goal}</p>
          <div className="flex flex-wrap gap-2">
            {strategy.marketing_channels.map((channel) => (
              <Badge key={channel} variant="secondary">
                {channel}
              </Badge>
            ))}
          </div>
        </CardContent>
      </Card>

      <div className="grid gap-4 lg:grid-cols-2">
        <Card>
          <CardHeader>
            <CardTitle className="text-base">Budget allocation</CardTitle>
          </CardHeader>
          <CardContent>
            <BudgetAllocationChart allocations={strategy.budget_allocation} />
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle className="text-base">Posts scheduled per channel</CardTitle>
          </CardHeader>
          <CardContent>
            <ChannelDistributionChart entries={strategy.content_calendar} />
          </CardContent>
        </Card>
      </div>

      <Card>
        <CardHeader>
          <CardTitle className="text-base">Content calendar timeline</CardTitle>
        </CardHeader>
        <CardContent>
          <CampaignTimelineChart entries={strategy.content_calendar} />
        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle className="text-base">Content themes</CardTitle>
        </CardHeader>
        <CardContent className="flex flex-wrap gap-2">
          {strategy.content_themes.map((theme) => (
            <Badge key={theme} variant="outline">
              {theme}
            </Badge>
          ))}
        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle className="text-base">Strategy summary</CardTitle>
        </CardHeader>
        <CardContent>
          <p className="text-sm leading-relaxed">{strategy.strategy_summary}</p>
        </CardContent>
      </Card>
    </div>
  );
}
