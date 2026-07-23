/**
 * Session-only campaign state.
 *
 * The backend intentionally has no database (see app/graph/coordinator.py
 * and the project's "no persistence" requirement) — every campaign the
 * API returns is a complete, self-contained CampaignResult. This context
 * is the frontend's equivalent of Streamlit's `st.session_state`: it just
 * keeps whatever's been generated *this browser session* in memory so the
 * Dashboard/Results/Observability pages can all reference the same data
 * without re-fetching anything that doesn't exist server-side.
 */

import { createContext, useCallback, useContext, useMemo, useState, type ReactNode } from "react";

import { ApiError, createCampaign } from "@/lib/api";
import type { CampaignRequest, CampaignResult } from "@/lib/types";

interface CampaignContextValue {
  /** Every campaign generated this session, newest first. */
  campaigns: CampaignResult[];
  /** The campaign currently shown on the Results/Observability pages. */
  currentCampaign: CampaignResult | null;
  isGenerating: boolean;
  error: string | null;
  generateCampaign: (request: CampaignRequest) => Promise<CampaignResult>;
  selectCampaign: (traceId: string) => void;
  clearError: () => void;
}

const CampaignContext = createContext<CampaignContextValue | undefined>(undefined);

export function CampaignProvider({ children }: { children: ReactNode }) {
  const [campaigns, setCampaigns] = useState<CampaignResult[]>([]);
  const [currentTraceId, setCurrentTraceId] = useState<string | null>(null);
  const [isGenerating, setIsGenerating] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const generateCampaign = useCallback(async (request: CampaignRequest) => {
    setIsGenerating(true);
    setError(null);
    try {
      const result = await createCampaign(request);
      setCampaigns((previous) => [result, ...previous]);
      setCurrentTraceId(result.trace_id);
      return result;
    } catch (caught) {
      const message = caught instanceof ApiError ? caught.message : "Something went wrong.";
      setError(message);
      throw caught;
    } finally {
      setIsGenerating(false);
    }
  }, []);

  const selectCampaign = useCallback((traceId: string) => {
    setCurrentTraceId(traceId);
  }, []);

  const clearError = useCallback(() => setError(null), []);

  const currentCampaign = useMemo(
    () => campaigns.find((campaign) => campaign.trace_id === currentTraceId) ?? null,
    [campaigns, currentTraceId]
  );

  const value = useMemo(
    () => ({ campaigns, currentCampaign, isGenerating, error, generateCampaign, selectCampaign, clearError }),
    [campaigns, currentCampaign, isGenerating, error, generateCampaign, selectCampaign, clearError]
  );

  return <CampaignContext.Provider value={value}>{children}</CampaignContext.Provider>;
}

export function useCampaign(): CampaignContextValue {
  const context = useContext(CampaignContext);
  if (!context) {
    throw new Error("useCampaign must be used within a CampaignProvider");
  }
  return context;
}
