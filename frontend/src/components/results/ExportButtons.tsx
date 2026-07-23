import { useState } from "react";
import { Download, FileText, Loader2 } from "lucide-react";
import { toast } from "sonner";

import { Button } from "@/components/ui/button";
import { ApiError, downloadBlob, exportCampaign } from "@/lib/api";
import { slugify } from "@/lib/utils";
import type { CampaignResult, ExportFormat } from "@/lib/types";

export function ExportButtons({ result }: { result: CampaignResult }) {
  const [pendingFormat, setPendingFormat] = useState<ExportFormat | null>(null);

  async function handleExport(format: ExportFormat) {
    setPendingFormat(format);
    try {
      const blob = await exportCampaign(result, format);
      const extension = format === "markdown" ? "md" : "pdf";
      downloadBlob(blob, `${slugify(result.request.product_name)}-campaign.${extension}`);
      toast.success(`Downloaded ${format === "markdown" ? "Markdown" : "PDF"} export`);
    } catch (error) {
      const message = error instanceof ApiError ? error.message : "Export failed.";
      toast.error(message);
    } finally {
      setPendingFormat(null);
    }
  }

  return (
    <div className="flex gap-2">
      <Button
        variant="outline"
        size="sm"
        disabled={pendingFormat !== null}
        onClick={() => handleExport("markdown")}
      >
        {pendingFormat === "markdown" ? (
          <Loader2 className="h-4 w-4 animate-spin" />
        ) : (
          <FileText className="h-4 w-4" />
        )}
        Markdown
      </Button>
      <Button variant="outline" size="sm" disabled={pendingFormat !== null} onClick={() => handleExport("pdf")}>
        {pendingFormat === "pdf" ? <Loader2 className="h-4 w-4 animate-spin" /> : <Download className="h-4 w-4" />}
        PDF
      </Button>
    </div>
  );
}
