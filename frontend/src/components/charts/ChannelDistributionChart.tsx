/**
 * How many content-calendar entries land on each channel — a plain
 * magnitude comparison, so it gets the safe default: one sequential hue,
 * no legend (single series — the axis labels already say what's plotted).
 */

import { useMemo } from "react";

import Plot from "@/lib/plotly";
import { baseLayout, CHART_CHROME, PLOTLY_CONFIG, SEQUENTIAL_HUE } from "@/lib/chartTheme";
import { useTheme } from "@/context/ThemeContext";
import type { ContentCalendarEntry } from "@/lib/types";

interface ChannelDistributionChartProps {
  entries: ContentCalendarEntry[];
}

export function ChannelDistributionChart({ entries }: ChannelDistributionChartProps) {
  const { theme } = useTheme();

  const { channels, counts } = useMemo(() => {
    const countByChannel = new Map<string, number>();
    for (const entry of entries) {
      countByChannel.set(entry.channel, (countByChannel.get(entry.channel) ?? 0) + 1);
    }
    const sorted = [...countByChannel.entries()].sort((a, b) => b[1] - a[1]);
    return { channels: sorted.map(([channel]) => channel), counts: sorted.map(([, count]) => count) };
  }, [entries]);

  if (entries.length === 0) {
    return <p className="py-8 text-center text-sm text-muted-foreground">No content calendar data.</p>;
  }

  const base = baseLayout(theme);
  const layout = {
    ...base,
    height: 260,
    showlegend: false,
    xaxis: { ...base.xaxis, title: "" },
    yaxis: { ...base.yaxis, title: "Scheduled posts", rangemode: "tozero", dtick: 1 },
    bargap: 0.4,
  };

  const trace = {
    type: "bar",
    x: channels,
    y: counts,
    text: counts.map(String),
    textposition: "outside",
    textfont: { color: CHART_CHROME[theme].secondaryInk },
    hovertemplate: "%{x}: %{y} scheduled post(s)<extra></extra>",
    marker: { color: SEQUENTIAL_HUE[theme] },
    width: 0.5,
  };

  return (
    <Plot data={[trace]} layout={layout} config={PLOTLY_CONFIG} style={{ width: "100%" }} useResizeHandler />
  );
}
