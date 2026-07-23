import { useNavigate } from "react-router-dom";
import { toast } from "sonner";

import { CampaignForm } from "@/components/campaign/CampaignForm";
import { ExecutionProgress } from "@/components/campaign/ExecutionProgress";
import { PageHeader } from "@/components/layout/PageHeader";
import { Card, CardContent } from "@/components/ui/card";
import { useCampaign } from "@/context/CampaignContext";
import type { CampaignRequest } from "@/lib/types";

export function NewCampaignPage() {
  const { generateCampaign, isGenerating } = useCampaign();
  const navigate = useNavigate();

  async function handleSubmit(request: CampaignRequest) {
    try {
      const result = await generateCampaign(request);
      toast.success("Campaign generated", {
        description: `Status: ${result.status}`,
      });
      navigate("/results");
    } catch (error) {
      const message = error instanceof Error ? error.message : "Something went wrong.";
      toast.error("Could not generate campaign", { description: message });
    }
  }

  return (
    <div>
      <PageHeader
        title="New Campaign"
        description="Describe your product and let the four-agent pipeline draft a full campaign."
      />

      {isGenerating ? (
        <ExecutionProgress />
      ) : (
        <Card>
          <CardContent className="pt-6">
            <CampaignForm onSubmit={handleSubmit} isSubmitting={isGenerating} />
          </CardContent>
        </Card>
      )}
    </div>
  );
}
