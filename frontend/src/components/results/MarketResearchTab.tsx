import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Separator } from "@/components/ui/separator";
import type { MarketIntelligenceReport } from "@/lib/types";

export function MarketResearchTab({ report }: { report: MarketIntelligenceReport | null | undefined }) {
  if (!report) {
    return <p className="text-sm text-muted-foreground">No market research was produced for this run.</p>;
  }

  return (
    <div className="grid gap-4 lg:grid-cols-2">
      <Card>
        <CardHeader>
          <CardTitle className="text-base">Target audience</CardTitle>
        </CardHeader>
        <CardContent>
          <p className="text-sm">{report.target_audience}</p>
        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle className="text-base">Competitors</CardTitle>
        </CardHeader>
        <CardContent className="space-y-3">
          {report.competitors.length === 0 && (
            <p className="text-sm text-muted-foreground">None identified.</p>
          )}
          {report.competitors.map((competitor) => (
            <div key={competitor.name}>
              <p className="text-sm font-medium">{competitor.name}</p>
              <p className="text-sm text-muted-foreground">{competitor.notes}</p>
            </div>
          ))}
        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle className="text-base">Market trends</CardTitle>
        </CardHeader>
        <CardContent>
          <ul className="list-inside list-disc space-y-1 text-sm">
            {report.market_trends.map((trend) => (
              <li key={trend}>{trend}</li>
            ))}
          </ul>
        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle className="text-base">Key insights</CardTitle>
        </CardHeader>
        <CardContent>
          <ul className="list-inside list-disc space-y-1 text-sm">
            {report.key_insights.map((insight) => (
              <li key={insight}>{insight}</li>
            ))}
          </ul>
        </CardContent>
      </Card>

      <Card className="lg:col-span-2">
        <CardHeader>
          <CardTitle className="text-base">Research summary</CardTitle>
        </CardHeader>
        <CardContent className="space-y-4">
          <p className="text-sm leading-relaxed">{report.summary}</p>

          {report.search_queries_used.length > 0 && (
            <>
              <Separator />
              <div>
                <p className="mb-2 text-xs font-medium uppercase tracking-wide text-muted-foreground">
                  Search queries used
                </p>
                <div className="flex flex-wrap gap-2">
                  {report.search_queries_used.map((query) => (
                    <Badge key={query} variant="secondary">
                      {query}
                    </Badge>
                  ))}
                </div>
              </div>
            </>
          )}

          {report.sources.length > 0 && (
            <>
              <Separator />
              <div>
                <p className="mb-2 text-xs font-medium uppercase tracking-wide text-muted-foreground">
                  Sources
                </p>
                <ul className="space-y-1 text-sm">
                  {report.sources.map((source) => (
                    <li key={source} className="truncate">
                      <a
                        href={source}
                        target="_blank"
                        rel="noreferrer"
                        className="text-primary hover:underline"
                      >
                        {source}
                      </a>
                    </li>
                  ))}
                </ul>
              </div>
            </>
          )}
        </CardContent>
      </Card>
    </div>
  );
}
