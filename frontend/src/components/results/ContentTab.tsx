import type { ReactNode } from "react";

import { Badge } from "@/components/ui/badge";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { CopyButton } from "@/components/ui/copy-button";
import type { ContentPackage } from "@/lib/types";

interface AssetCardProps {
  title: string;
  copyValue: string;
  children: ReactNode;
}

function AssetCard({ title, copyValue, children }: AssetCardProps) {
  return (
    <Card>
      <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
        <CardTitle className="text-base">{title}</CardTitle>
        <CopyButton value={copyValue} />
      </CardHeader>
      <CardContent>{children}</CardContent>
    </Card>
  );
}

export function ContentTab({ content }: { content: ContentPackage | null | undefined }) {
  if (!content) {
    return <p className="text-sm text-muted-foreground">No content package was produced for this run.</p>;
  }

  return (
    <div className="space-y-4">
      <Card>
        <CardHeader>
          <CardTitle className="text-base">Brand voice</CardTitle>
        </CardHeader>
        <CardContent className="space-y-2">
          <p className="text-sm">
            <span className="font-medium">{content.brand_voice.tone}</span> —{" "}
            {content.brand_voice.voice_description}
          </p>
          <div className="flex flex-wrap gap-2">
            {content.brand_voice.style_keywords.map((keyword) => (
              <Badge key={keyword} variant="secondary">
                {keyword}
              </Badge>
            ))}
          </div>
        </CardContent>
      </Card>

      <div className="grid gap-4 lg:grid-cols-2">
        <AssetCard title="Instagram caption" copyValue={content.instagram_caption}>
          <p className="whitespace-pre-wrap text-sm">{content.instagram_caption}</p>
        </AssetCard>

        <AssetCard title="X post" copyValue={content.x_post}>
          <p className="whitespace-pre-wrap text-sm">{content.x_post}</p>
          <p className="mt-2 text-xs text-muted-foreground">{content.x_post.length}/280 characters</p>
        </AssetCard>

        <AssetCard title="LinkedIn post" copyValue={content.linkedin_post}>
          <p className="whitespace-pre-wrap text-sm">{content.linkedin_post}</p>
        </AssetCard>

        <AssetCard
          title="Email campaign"
          copyValue={`${content.email_campaign.subject_line}\n\n${content.email_campaign.body}`}
        >
          <p className="text-sm font-medium">{content.email_campaign.subject_line}</p>
          <p className="mt-2 whitespace-pre-wrap text-sm text-muted-foreground">
            {content.email_campaign.body}
          </p>
        </AssetCard>
      </div>

      <div className="grid gap-4 lg:grid-cols-3">
        <AssetCard title="Ad headlines" copyValue={content.ad_headlines.join("\n")}>
          <ul className="list-inside list-disc space-y-1 text-sm">
            {content.ad_headlines.map((headline) => (
              <li key={headline}>{headline}</li>
            ))}
          </ul>
        </AssetCard>

        <AssetCard title="Hashtags" copyValue={content.hashtags.join(" ")}>
          <div className="flex flex-wrap gap-2">
            {content.hashtags.map((hashtag) => (
              <Badge key={hashtag} variant="outline">
                {hashtag}
              </Badge>
            ))}
          </div>
        </AssetCard>

        <AssetCard title="Call to action" copyValue={content.call_to_action}>
          <p className="text-sm font-medium">{content.call_to_action}</p>
        </AssetCard>
      </div>
    </div>
  );
}
