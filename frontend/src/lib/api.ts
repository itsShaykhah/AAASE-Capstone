/**
 * Typed HTTP client for the FastAPI backend (app/api/routes/*.py).
 *
 * This is the only file that knows the backend's actual routes/shapes —
 * every component calls the functions here, never axios directly. That
 * keeps the API contract in one place, matching how the old Streamlit
 * frontend's `api_client.py` was the single HTTP boundary on the Python
 * side (see app/frontend, now removed in favor of this app).
 */

import axios, { AxiosError } from "axios";

import type { CampaignRequest, CampaignResult, ExportFormat } from "@/lib/types";

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL ?? "http://127.0.0.1:8000";

export const apiClient = axios.create({
  baseURL: API_BASE_URL,
  timeout: 180_000, // the pipeline runs four sequential LLM calls; give it room
});

/** Raised for both guardrail-blocked requests (422) and transport failures. */
export class ApiError extends Error {
  readonly status?: number;

  constructor(message: string, status?: number) {
    super(message);
    this.name = "ApiError";
    this.status = status;
  }
}

function toApiError(error: unknown): ApiError {
  if (axios.isAxiosError(error)) {
    const axiosError = error as AxiosError<{ detail?: string }>;
    const detail = axiosError.response?.data?.detail;
    if (axiosError.response?.status === 422 && detail) {
      return new ApiError(detail, 422);
    }
    if (axiosError.response) {
      return new ApiError(
        `The API responded with an error (${axiosError.response.status}).`,
        axiosError.response.status
      );
    }
    return new ApiError(`Could not reach the API at ${API_BASE_URL}. Is the backend running?`);
  }
  return new ApiError("An unexpected error occurred.");
}

export async function checkHealth(): Promise<boolean> {
  try {
    const response = await apiClient.get("/health");
    return response.status === 200;
  } catch {
    return false;
  }
}

export async function createCampaign(request: CampaignRequest): Promise<CampaignResult> {
  try {
    const response = await apiClient.post<CampaignResult>("/api/campaigns", request);
    return response.data;
  } catch (error) {
    throw toApiError(error);
  }
}

export async function exportCampaign(result: CampaignResult, format: ExportFormat): Promise<Blob> {
  try {
    const response = await apiClient.post(`/api/campaigns/export/${format}`, result, {
      responseType: "blob",
    });
    return response.data as Blob;
  } catch (error) {
    throw toApiError(error);
  }
}

/** Triggers a browser download for an exported file without a server round trip for the save itself. */
export function downloadBlob(blob: Blob, filename: string): void {
  const url = URL.createObjectURL(blob);
  const link = document.createElement("a");
  link.href = url;
  link.download = filename;
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);
  URL.revokeObjectURL(url);
}
