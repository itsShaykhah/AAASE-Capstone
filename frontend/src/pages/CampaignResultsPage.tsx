import { FileQuestion } from "lucide-react";
import { NavLink } from "react-router-dom";

import { ContentTab } from "@/components/results/ContentTab";
import { ExportButtons } from "@/components/results/ExportButtons";
import { MarketResearchTab } from "@/components/results/MarketResearchTab";
import { QualityReviewTab } from "@/components/results/QualityReviewTab";
import { StrategyTab } from "@/components/results/StrategyTab";
import { PageHeader } from "@/components/layout/PageHeader";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { useCampaign } from "@/context/CampaignContext";
import { formatDateTime } from "@/lib/utils";

const STATUS_BADGE_VARIANT: Record<string, "success" | "warning" | "destructive" | "secondary"> = {
  completed: "success",
  failed: "destructive",
  blocked: "warning",
  in_progress: "secondary",
  pending: "secondary",
};

export function CampaignResultsPage() {
  const { currentCampaign } = useCampaign();

  if (!currentCampaign) {
    return (
      <div>
        <PageHeader title="Campaign Results" />
        <div className="flex flex-col items-center justify-center gap-4 rounded-xl border border-dashed py-24 text-center">
          <FileQuestion className="h-10 w-10 text-muted-foreground" />
          <div>
            <p className="font-medium">No campaign selected yet</p>
            <p className="text-sm text-muted-foreground">Generate a campaign to see its results here.</p>
          </div>
          <Button asChild>
            <NavLink to="/new-campaign">Create a campaign</NavLink>
          </Button>
        </div>
      </div>
    );
  }

  const finalContent = currentCampaign.quality_review?.final_content ?? currentCampaign.content_package;

  return (
    <div>
      <PageHeader
        title={currentCampaign.request.product_name}
        description={`Generated ${formatDateTime(currentCampaign.generated_at)}`}
        actions={
          <>
            <Badge variant={STATUS_BADGE_VARIANT[currentCampaign.status] ?? "secondary"}>
              {currentCampaign.status.replace(/_/g, " ")}
            </Badge>
            <ExportButtons result={currentCampaign} />
          </>
        }
      />

      <Tabs defaultValue="research">
        <TabsList>
          <TabsTrigger value="research">Market Research</TabsTrigger>
          <TabsTrigger value="strategy">Strategy</TabsTrigger>
          <TabsTrigger value="content">Content</TabsTrigger>
          <TabsTrigger value="quality">Quality Review</TabsTrigger>
        </TabsList>

        <TabsContent value="research">
          <MarketResearchTab report={currentCampaign.market_intelligence} />
        </TabsContent>
        <TabsContent value="strategy">
          <StrategyTab strategy={currentCampaign.campaign_strategy} />
        </TabsContent>
        <TabsContent value="content">
          <ContentTab content={finalContent} />
        </TabsContent>
        <TabsContent value="quality">
          <QualityReviewTab review={currentCampaign.quality_review} />
        </TabsContent>
      </Tabs>
    </div>
  );
}
