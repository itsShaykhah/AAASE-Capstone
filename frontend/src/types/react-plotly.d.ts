/**
 * Minimal ambient typing for `react-plotly.js` (used via its `/factory`
 * entry point so charts bundle the lighter `plotly.js-dist-min` instead of
 * the full `plotly.js` package — see src/lib/plotly.ts).
 *
 * No dependency on `@types/react-plotly.js`: this project only touches a
 * handful of props (data/layout/config/style), so a small hand-written
 * declaration avoids pulling in a whole community types package purely
 * for the four small chart wrappers under src/components/charts.
 */

declare module "react-plotly.js/factory" {
  import type { Component } from "react";

  export interface PlotParams {
    data: unknown[];
    layout?: Record<string, unknown>;
    config?: Record<string, unknown>;
    style?: React.CSSProperties;
    className?: string;
    useResizeHandler?: boolean;
  }

  export default function createPlotlyComponent(
    plotly: unknown
  ): new (props: PlotParams) => Component<PlotParams>;
}

declare module "plotly.js-dist-min" {
  const Plotly: unknown;
  export default Plotly;
}
