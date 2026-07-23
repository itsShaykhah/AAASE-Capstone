/**
 * Content calendar as a timeline: each channel gets its own horizontal
 * lane, entries plotted by day. Channels are a fixed small set (identity,
 * not magnitude), so this uses the categorical palette in its validated
 * order, one series per channel — safe up to 8 lanes before folding into
 * "Other". Themes aren't drawn as on-chart text for every marker (that's
 * the "never label every point" rule); they live in the hover tooltip and
 * the content-calendar table alongside this chart.
 */

import { useMemo } from "react";

import Plot from "@/lib/plotly";
import { baseLayout, categoricalColor, PLOTLY_CONFIG } from "@/lib/chartTheme";
import { useTheme } from "@/context/ThemeContext";
import type { ContentCalendarEntry } from "@/lib/types";

interface CampaignTimelineChartProps {
  entries: ContentCalendarEntry[];
}

export function CampaignTimelineChart({ entries }: CampaignTimelineChartProps) {
  const { theme } = useTheme();

  const { traces, channels } = useMemo(() => {
    const channelOrder = [...new Set(entries.map((entry) => entry.channel))];
    const builtTraces = channelOrder.map((channel, index) => {
      const channelEntries = entries.filter((entry) => entry.channel === channel);
      return {
        type: "scatter",
        mode: "markers",
        name: channel,
        x: channelEntries.map((entry) => entry.day),
        y: channelEntries.map(() => channel),
        text: channelEntries.map((entry) => entry.theme),
        hovertemplate: `Day %{x} — ${channel}<br>%{text}<extra></extra>`,
        marker: { color: categoricalColor(index, theme), size: 14, symbol: "circle" },
      };
    });
    return { traces: builtTraces, channels: channelOrder };
  }, [entries, theme]);

  if (entries.length === 0) {
    return <p className="py-8 text-center text-sm text-muted-foreground">No content calendar data.</p>;
  }

  const base = baseLayout(theme);
  const layout = {
    ...base,
    height: 120 + channels.length * 48,
    showlegend: channels.length > 1,
    margin: { t: 8, r: 16, b: 32, l: 140 },
    xaxis: { ...base.xaxis, title: "Campaign day", rangemode: "tozero", dtick: 1 },
    yaxis: { ...base.yaxis, automargin: true, type: "category" },
  };

  return (
    <Plot data={traces} layout={layout} config={PLOTLY_CONFIG} style={{ width: "100%" }} useResizeHandler />
  );
}
