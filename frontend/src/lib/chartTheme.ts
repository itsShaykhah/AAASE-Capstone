/**
 * Chart color tokens and shared Plotly layout defaults.
 *
 * Values are copied verbatim from the data-viz skill's validated reference
 * palette (categorical order, sequential blue ramp, chart chrome) rather
 * than invented — the categorical order in particular is a CVD-safety
 * mechanism (validated adjacent-pair contrast), not a cosmetic choice, so
 * it must stay in this exact order rather than being re-sorted per chart.
 */

export type ThemeMode = "light" | "dark";

/** Fixed categorical order — never re-sort or cycle past what a chart needs. */
export const CATEGORICAL_PALETTE: Record<ThemeMode, string[]> = {
  light: ["#2a78d6", "#eb6834", "#1baf7a", "#eda100", "#e87ba4", "#008300", "#4a3aa7", "#e34948"],
  dark: ["#3987e5", "#d95926", "#199e70", "#c98500", "#d55181", "#008300", "#9085e9", "#e66767"],
};

/** Single-hue blue, used for plain magnitude comparisons (bar/column charts). */
export const SEQUENTIAL_HUE: Record<ThemeMode, string> = {
  light: "#2a78d6",
  dark: "#3987e5",
};

/** Fixed status colors — reserved for state, never reused as a categorical slot. */
export const STATUS_COLORS = {
  good: "#0ca30c",
  warning: "#fab219",
  serious: "#ec835a",
  critical: "#d03b3b",
} as const;

interface ChartChrome {
  surface: string;
  primaryInk: string;
  secondaryInk: string;
  mutedInk: string;
  gridline: string;
  axisLine: string;
}

export const CHART_CHROME: Record<ThemeMode, ChartChrome> = {
  light: {
    surface: "#fcfcfb",
    primaryInk: "#0b0b0b",
    secondaryInk: "#52514e",
    mutedInk: "#898781",
    gridline: "#e1e0d9",
    axisLine: "#c3c2b7",
  },
  dark: {
    surface: "#1a1a19",
    primaryInk: "#ffffff",
    secondaryInk: "#c3c2b7",
    mutedInk: "#898781",
    gridline: "#2c2c2a",
    axisLine: "#383835",
  },
};

/** Categorical color for the Nth series, wrapping only if a chart ever
 * legitimately needs more than 8 (it shouldn't — fold extras into "Other"). */
export function categoricalColor(index: number, mode: ThemeMode): string {
  const palette = CATEGORICAL_PALETTE[mode];
  return palette[index % palette.length];
}

/** Plain record type for every nested Plotly layout field below — keeps
 * `baseLayout(...).xaxis` (etc.) spreadable, rather than widening to
 * `unknown` the way a blanket `Record<string, unknown>` return type would. */
type PlotlyDict = Record<string, unknown>;

export interface BaseChartLayout extends PlotlyDict {
  paper_bgcolor: string;
  plot_bgcolor: string;
  font: PlotlyDict;
  margin: PlotlyDict;
  xaxis: PlotlyDict;
  yaxis: PlotlyDict;
  legend: PlotlyDict;
  hoverlabel: PlotlyDict;
}

/** Shared Plotly layout: transparent-to-card surface, recessive hairline
 * gridlines, no second axis, consistent typography. Merge chart-specific
 * fields (axis titles, margins) on top of this — call once per render and
 * reuse the result rather than calling `baseLayout` again for each field. */
export function baseLayout(mode: ThemeMode): BaseChartLayout {
  const chrome = CHART_CHROME[mode];
  return {
    paper_bgcolor: "transparent",
    plot_bgcolor: "transparent",
    font: {
      family: "system-ui, -apple-system, 'Segoe UI', sans-serif",
      color: chrome.secondaryInk,
      size: 12,
    },
    margin: { t: 24, r: 16, b: 40, l: 8 },
    xaxis: {
      gridcolor: chrome.gridline,
      linecolor: chrome.axisLine,
      zerolinecolor: chrome.axisLine,
      tickfont: { color: chrome.mutedInk },
    },
    yaxis: {
      gridcolor: chrome.gridline,
      linecolor: chrome.axisLine,
      zerolinecolor: chrome.axisLine,
      tickfont: { color: chrome.mutedInk },
    },
    legend: {
      orientation: "h",
      y: -0.2,
      font: { color: chrome.secondaryInk },
    },
    hoverlabel: {
      bgcolor: chrome.surface,
      bordercolor: chrome.axisLine,
      font: { color: chrome.primaryInk },
    },
  };
}

// Typed as Record<string, unknown> up front (not `as const`) so it's
// directly assignable to PlotParams["config"] without TS complaining about
// a missing index signature on a narrowly-typed named constant.
export const PLOTLY_CONFIG: Record<string, unknown> = {
  displayModeBar: false,
  responsive: true,
};
