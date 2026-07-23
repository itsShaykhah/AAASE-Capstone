/**
 * Budget allocation: a part-to-whole question, so this is a single
 * horizontal 100%-stacked bar (one segment per channel) rather than a pie
 * — see the data-viz skill's form table ("part-to-whole -> stacked bar,
 * horizontal for long category names"). Colored by the fixed categorical
 * order; a legend carries identity since there are 2+ segments.
 */

import { useMemo } from "react";

import Plot from "@/lib/plotly";
import { baseLayout, categoricalColor, PLOTLY_CONFIG } from "@/lib/chartTheme";
import { useTheme } from "@/context/ThemeContext";
import type { BudgetAllocation } from "@/lib/types";

interface BudgetAllocationChartProps {
  allocations: BudgetAllocation[];
}

export function BudgetAllocationChart({ allocations }: BudgetAllocationChartProps) {
  const { theme } = useTheme();

  const traces = useMemo(
    () =>
      allocations.map((allocation, index) => ({
        type: "bar",
        orientation: "h",
        name: allocation.channel,
        x: [allocation.percentage],
        y: ["Budget"],
        text: [`${allocation.channel} — ${allocation.percentage.toFixed(0)}%`],
        textposition: "inside",
        insidetextanchor: "middle",
        hovertemplate: `${allocation.channel}: %{x:.0f}%<extra></extra>`,
        marker: { color: categoricalColor(index, theme) },
      })),
    [allocations, theme]
  );

  if (allocations.length === 0) {
    return <p className="py-8 text-center text-sm text-muted-foreground">No budget allocation data.</p>;
  }

  const base = baseLayout(theme);
  const layout = {
    ...base,
    barmode: "stack",
    showlegend: true,
    height: 160,
    margin: { t: 8, r: 16, b: 8, l: 8 },
    xaxis: { ...base.xaxis, visible: false, range: [0, 100] },
    yaxis: { ...base.yaxis, visible: false },
  };

  return (
    <Plot data={traces} layout={layout} config={PLOTLY_CONFIG} style={{ width: "100%" }} useResizeHandler />
  );
}
