/**
 * TypeScript mirror of the FastAPI/Pydantic schemas in app/schemas/*.py.
 *
 * Kept as one file, hand-mirrored rather than generated, because the
 * backend is intentionally not being touched by this frontend rewrite
 * (see app/schemas/). If the backend schemas change, update this file to
 * match — it's the single place the rest of the frontend imports types
 * from, so a mismatch surfaces here first as a type error, not at runtime.
 */

export type CampaignObjective =
  | "brand_awareness"
  | "lead_generation"
  | "sales_conversion"
  | "product_launch"
  | "customer_engagement";

export const CAMPAIGN_OBJECTIVES: { value: CampaignObjective; label: string }[] = [
  { value: "brand_awareness", label: "Brand Awareness" },
  { value: "lead_generation", label: "Lead Generation" },
  { value: "sales_conversion", label: "Sales Conversion" },
  { value: "product_launch", label: "Product Launch" },
  { value: "customer_engagement", label: "Customer Engagement" },
];

export type CampaignStatus = "pending" | "in_progress" | "completed" | "failed" | "blocked";

export type QualityCheckStatus = "passed" | "needs_attention" | "failed";

export type AgentKey =
  | "market_intelligence"
  | "campaign_strategy"
  | "content_generation"
  | "quality_assurance";

export const AGENT_LABELS: Record<AgentKey, string> = {
  market_intelligence: "Market Intelligence",
  campaign_strategy: "Campaign Strategy",
  content_generation: "Content Generation",
  quality_assurance: "Quality Assurance",
};

export const AGENT_ORDER: AgentKey[] = [
  "market_intelligence",
  "campaign_strategy",
  "content_generation",
  "quality_assurance",
];

// --- Request ---------------------------------------------------------------

export interface CampaignRequest {
  product_name: string;
  product_description: string;
  campaign_objective: CampaignObjective;
  target_audience?: string | null;
  campaign_duration_days?: number | null;
  brand_tone?: string | null;
  additional_notes?: string | null;
}

// --- Market Intelligence ----------------------------------------------------

export interface Competitor {
  name: string;
  notes: string;
}

export interface MarketIntelligenceReport {
  target_audience: string;
  competitors: Competitor[];
  market_trends: string[];
  key_insights: string[];
  summary: string;
  search_queries_used: string[];
  sources: string[];
}

// --- Campaign Strategy -------------------------------------------------------

export interface ContentCalendarEntry {
  day: number;
  channel: string;
  theme: string;
}

export interface BudgetAllocation {
  channel: string;
  percentage: number;
}

export interface CampaignStrategy {
  campaign_goal: string;
  marketing_channels: string[];
  content_calendar: ContentCalendarEntry[];
  content_themes: string[];
  budget_allocation: BudgetAllocation[];
  strategy_summary: string;
}

// --- Content Package ---------------------------------------------------------

export interface BrandVoice {
  tone: string;
  style_keywords: string[];
  voice_description: string;
}

export interface EmailCampaign {
  subject_line: string;
  body: string;
}

export interface ContentPackage {
  brand_voice: BrandVoice;
  instagram_caption: string;
  x_post: string;
  linkedin_post: string;
  email_campaign: EmailCampaign;
  ad_headlines: string[];
  hashtags: string[];
  call_to_action: string;
}

// --- Quality Review ------------------------------------------------------------

export interface QualityCheckResult {
  check_name: string;
  status: QualityCheckStatus;
  notes: string;
}

export interface QualityReview {
  checks: QualityCheckResult[];
  overall_approved: boolean;
  final_notes: string;
  final_content: ContentPackage;
}

// --- Observability ---------------------------------------------------------

export interface ObservabilityEvent {
  trace_id: string;
  event: string;
  timestamp: string;
  agent?: string;
  duration_ms?: number;
  provider?: string | null;
  reason?: string;
  query?: string;
  error?: string;
  [key: string]: unknown;
}

export interface ObservabilitySummary {
  trace_id: string;
  total_duration_ms: number;
  agent_durations_ms: Record<string, number>;
  provider_used: Record<string, string>;
  errors: string[];
  events: ObservabilityEvent[];
}

// --- Aggregate result --------------------------------------------------------

export interface CampaignResult {
  trace_id: string;
  status: CampaignStatus;
  request: CampaignRequest;
  market_intelligence?: MarketIntelligenceReport | null;
  campaign_strategy?: CampaignStrategy | null;
  content_package?: ContentPackage | null;
  quality_review?: QualityReview | null;
  observability: ObservabilitySummary;
  generated_at: string;
}

export type ExportFormat = "markdown" | "pdf";
