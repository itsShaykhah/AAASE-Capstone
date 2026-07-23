import { AlertTriangle, CheckCircle2, XCircle } from "lucide-react";
import type { ReactNode } from "react";

import { Badge } from "@/components/ui/badge";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import type { QualityCheckStatus, QualityReview } from "@/lib/types";

const STATUS_ICON: Record<QualityCheckStatus, ReactNode> = {
  passed: <CheckCircle2 className="h-4 w-4 text-success" />,
  needs_attention: <AlertTriangle className="h-4 w-4 text-warning" />,
  failed: <XCircle className="h-4 w-4 text-destructive" />,
};

const STATUS_BADGE_VARIANT: Record<QualityCheckStatus, "success" | "warning" | "destructive"> = {
  passed: "success",
  needs_attention: "warning",
  failed: "destructive",
};

export function QualityReviewTab({ review }: { review: QualityReview | null | undefined }) {
  if (!review) {
    return <p className="text-sm text-muted-foreground">No quality review was produced for this run.</p>;
  }

  return (
    <div className="space-y-4">
      <Card>
        <CardHeader className="flex flex-row items-center justify-between space-y-0">
          <CardTitle className="text-base">Overall approval</CardTitle>
          <Badge variant={review.overall_approved ? "success" : "warning"} className="text-sm">
            {review.overall_approved ? "Approved" : "Needs revision"}
          </Badge>
        </CardHeader>
        <CardContent>
          <p className="text-sm leading-relaxed">{review.final_notes}</p>
        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle className="text-base">Checks</CardTitle>
        </CardHeader>
        <CardContent className="space-y-3">
          {review.checks.map((check) => (
            <div
              key={check.check_name}
              className="flex items-start justify-between gap-4 rounded-lg border p-3"
            >
              <div className="flex items-start gap-3">
                {STATUS_ICON[check.status]}
                <div>
                  <p className="text-sm font-medium capitalize">{check.check_name.replace(/_/g, " ")}</p>
                  <p className="text-sm text-muted-foreground">{check.notes}</p>
                </div>
              </div>
              <Badge variant={STATUS_BADGE_VARIANT[check.status]} className="shrink-0">
                {check.status.replace(/_/g, " ")}
              </Badge>
            </div>
          ))}
        </CardContent>
      </Card>
    </div>
  );
}
