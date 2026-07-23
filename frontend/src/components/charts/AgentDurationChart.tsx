/**
 * Per-agent execution time — magnitude comparison across long labels
 * ("Market Intelligence", "Campaign Strategy", ...), so horizontal bars,
 * one sequential hue, value labeled at the bar tip.
 */

import { useMemo } from "react";

import Plot from "@/lib/plotly";
import { baseLayout, CHART_CHROME, PLOTLY_CONFIG, SEQUENTIAL_HUE } from "@/lib/chartTheme";
import { useTheme } from "@/context/ThemeContext";
import { AGENT_LABELS, AGENT_ORDER, type AgentKey } from "@/lib/types";
import { formatDuration } from "@/lib/utils";

interface AgentDurationChartProps {
  agentDurationsMs: Record<string, number>;
}

export function AgentDurationChart({ agentDurationsMs }: AgentDurationChartProps) {
  const { theme } = useTheme();

  const { labels, values } = useMemo(() => {
    const orderedKeys = AGENT_ORDER.filter((key) => key in agentDurationsMs);
    // Plotly draws horizontal bars bottom-to-top, so reverse to read
    // top-to-bottom in pipeline order (Market Intelligence first).
    const keys = [...orderedKeys].reverse();
    return {
      labels: keys.map((key) => AGENT_LABELS[key as AgentKey] ?? key),
      values: keys.map((key) => agentDurationsMs[key]),
    };
  }, [agentDurationsMs]);

  if (labels.length === 0) {
    return <p className="py-8 text-center text-sm text-muted-foreground">No execution timing data yet.</p>;
  }

  const base = baseLayout(theme);
  const layout = {
    ...base,
    height: 220,
    showlegend: false,
    margin: { t: 8, r: 48, b: 32, l: 140 },
    xaxis: { ...base.xaxis, title: "Duration", rangemode: "tozero" },
    yaxis: { ...base.yaxis, automargin: true },
  };

  const trace = {
    type: "bar",
    orientation: "h",
    x: values,
    y: labels,
    text: values.map(formatDuration),
    textposition: "outside",
    textfont: { color: CHART_CHROME[theme].secondaryInk },
    hovertemplate: "%{y}: %{text}<extra></extra>",
    marker: { color: SEQUENTIAL_HUE[theme] },
    width: 0.5,
  };

  return (
    <Plot data={[trace]} layout={layout} config={PLOTLY_CONFIG} style={{ width: "100%" }} useResizeHandler />
  );
}
