/**
 * Shared Plot component, built from the lightweight `plotly.js-dist-min`
 * bundle rather than the full `plotly.js` package `react-plotly.js`
 * depends on by default — meaningfully smaller production bundle for a
 * SPA that only needs bar/pie/timeline traces.
 */

import Plotly from "plotly.js-dist-min";
import createPlotlyComponent from "react-plotly.js/factory";

const Plot = createPlotlyComponent(Plotly);

export default Plot;
