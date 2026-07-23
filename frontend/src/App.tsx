import { BrowserRouter, Route, Routes } from "react-router-dom";
import { Toaster } from "sonner";

import { AppShell } from "@/components/layout/AppShell";
import { CampaignProvider } from "@/context/CampaignContext";
import { ThemeProvider } from "@/context/ThemeContext";
import { AboutPage } from "@/pages/AboutPage";
import { CampaignResultsPage } from "@/pages/CampaignResultsPage";
import { DashboardPage } from "@/pages/DashboardPage";
import { NewCampaignPage } from "@/pages/NewCampaignPage";
import { ObservabilityPage } from "@/pages/ObservabilityPage";

export default function App() {
  return (
    <ThemeProvider>
      <CampaignProvider>
        <BrowserRouter>
          <Routes>
            <Route element={<AppShell />}>
              <Route index element={<DashboardPage />} />
              <Route path="new-campaign" element={<NewCampaignPage />} />
              <Route path="results" element={<CampaignResultsPage />} />
              <Route path="observability" element={<ObservabilityPage />} />
              <Route path="about" element={<AboutPage />} />
            </Route>
          </Routes>
        </BrowserRouter>
        <Toaster richColors position="top-right" />
      </CampaignProvider>
    </ThemeProvider>
  );
}
