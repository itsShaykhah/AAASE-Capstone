import { CheckCircle2, Clock, Megaphone, Sparkles } from "lucide-react";
import { useNavigate } from "react-router-dom";

import { PageHeader } from "@/components/layout/PageHeader";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table";
import { useCampaign } from "@/context/CampaignContext";
import { CAMPAIGN_OBJECTIVES } from "@/lib/types";
import { formatDateTime, formatDuration } from "@/lib/utils";

const STATUS_BADGE_VARIANT: Record<string, "success" | "warning" | "destructive" | "secondary"> = {
  completed: "success",
  failed: "destructive",
  blocked: "warning",
  in_progress: "secondary",
  pending: "secondary",
};

function objectiveLabel(value: string): string {
  return CAMPAIGN_OBJECTIVES.find((option) => option.value === value)?.label ?? value;
}

export function DashboardPage() {
  const { campaigns, selectCampaign } = useCampaign();
  const navigate = useNavigate();

  const totalCampaigns = campaigns.length;
  const approvedCount = campaigns.filter((c) => c.quality_review?.overall_approved).length;
  const avgDurationMs =
    totalCampaigns > 0
      ? campaigns.reduce((sum, c) => sum + c.observability.total_duration_ms, 0) / totalCampaigns
      : 0;

  function viewCampaign(traceId: string) {
    selectCampaign(traceId);
    navigate("/results");
  }

  return (
    <div className="space-y-6">
      <PageHeader
        title="Dashboard"
        description="Session overview of the campaigns you've generated."
        actions={
          <Button onClick={() => navigate("/new-campaign")}>
            <Sparkles className="h-4 w-4" />
            New Campaign
          </Button>
        }
      />

      <div className="grid gap-4 sm:grid-cols-3">
        <Card>
          <CardContent className="flex items-center gap-4 p-4">
            <div className="flex h-10 w-10 items-center justify-center rounded-lg bg-primary/10 text-primary">
              <Megaphone className="h-5 w-5" />
            </div>
            <div>
              <p className="text-xs text-muted-foreground">Campaigns this session</p>
              <p className="text-lg font-semibold">{totalCampaigns}</p>
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardContent className="flex items-center gap-4 p-4">
            <div className="flex h-10 w-10 items-center justify-center rounded-lg bg-primary/10 text-primary">
              <Clock className="h-5 w-5" />
            </div>
            <div>
              <p className="text-xs text-muted-foreground">Average generation time</p>
              <p className="text-lg font-semibold">
                {totalCampaigns > 0 ? formatDuration(avgDurationMs) : "—"}
              </p>
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardContent className="flex items-center gap-4 p-4">
            <div className="flex h-10 w-10 items-center justify-center rounded-lg bg-success/15 text-success">
              <CheckCircle2 className="h-5 w-5" />
            </div>
            <div>
              <p className="text-xs text-muted-foreground">QA-approved</p>
              <p className="text-lg font-semibold">
                {totalCampaigns > 0 ? `${approvedCount}/${totalCampaigns}` : "—"}
              </p>
            </div>
          </CardContent>
        </Card>
      </div>

      <Card>
        <CardHeader>
          <CardTitle className="text-base">Recent campaigns</CardTitle>
        </CardHeader>
        <CardContent>
          {campaigns.length === 0 ? (
            <div className="flex flex-col items-center gap-3 py-12 text-center">
              <p className="text-sm text-muted-foreground">
                Nothing generated yet this session — start with a product brief.
              </p>
              <Button onClick={() => navigate("/new-campaign")}>Create your first campaign</Button>
            </div>
          ) : (
            <Table>
              <TableHeader>
                <TableRow>
                  <TableHead>Product</TableHead>
                  <TableHead>Objective</TableHead>
                  <TableHead>Status</TableHead>
                  <TableHead>Generated</TableHead>
                  <TableHead>Duration</TableHead>
                  <TableHead />
                </TableRow>
              </TableHeader>
              <TableBody>
                {campaigns.map((campaign) => (
                  <TableRow key={campaign.trace_id}>
                    <TableCell className="font-medium">{campaign.request.product_name}</TableCell>
                    <TableCell className="text-sm text-muted-foreground">
                      {objectiveLabel(campaign.request.campaign_objective)}
                    </TableCell>
                    <TableCell>
                      <Badge variant={STATUS_BADGE_VARIANT[campaign.status] ?? "secondary"}>
                        {campaign.status.replace(/_/g, " ")}
                      </Badge>
                    </TableCell>
                    <TableCell className="whitespace-nowrap text-sm text-muted-foreground">
                      {formatDateTime(campaign.generated_at)}
                    </TableCell>
                    <TableCell className="text-sm text-muted-foreground">
                      {formatDuration(campaign.observability.total_duration_ms)}
                    </TableCell>
                    <TableCell>
                      <Button variant="ghost" size="sm" onClick={() => viewCampaign(campaign.trace_id)}>
                        View
                      </Button>
                    </TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          )}
        </CardContent>
      </Card>
    </div>
  );
}
