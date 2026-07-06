const API_BASE = import.meta.env.VITE_API_URL || 'http://localhost:8000';

export interface DiscoverRequest {
  query: string;
  language: 'en' | 'hi';
  session_id?: string;
}

export interface DecisionAnalysis {
  eligibility?: string;
  suitability?: string;
  difficulty?: string;
  confidence?: string;
  recommendation?: string;
  risk?: string;
  overall_recommendation?: string;
  why_recommended?: string;
  why_not_fit?: string;
  overview?: string;
  who_can_apply?: string;
  required_qualification?: string;
  minimum_cgpa?: string;
  required_experience?: string;
  documents_required?: string;
  funding_details?: Record<string, string>;
  application_process?: string;
  selection_process?: string;
  application_fees?: string;
  official_deadline?: string;
  official_source?: string;
  verified_date?: string;
  application_link?: string;
  status?: string;
  eligibility_analysis?: {
    academic_match?: string;
    language_match?: string;
    experience_match?: string;
    funding_match?: string;
    degree_match?: string;
  };
}

export interface Opportunity {
  id?: string;
  title: string;
  provider: string;
  country?: string;
  category: string;
  degree?: string;
  funding_type?: string;
  deadline?: string;
  eligibility?: string;
  description?: string;
  official_url?: string;
  verification: Record<string, unknown>;
  source_type: string;
  match_score?: number;
  decision_analysis?: DecisionAnalysis;
  next_steps?: string[];
}

export interface DiscoverResponse {
  query: string;
  language: string;
  thinking_steps: string[];
  summary: string;
  roadmap: string[];
  opportunities: Opportunity[];
  verification_summary: { status: string; sources_checked: number; official_sources: number };
  official_links: string[];
  timings: Record<string, number>;
  generated_at: string;
  intent?: string;
  missing_information?: string[];
  total_found?: number;
  verified_count?: number;
  decision_summary?: string;
  follow_up_questions?: string[];
  follow_up_required?: boolean;
  ai_explanation_available?: boolean;
  alternatives?: Array<{ type: string; title: string; provider: string; country?: string; reason: string; advantage: string; official_url?: string }>;
  action_checklist?: string[];
}

const SESSION_KEY = 'opportunityos_session_id';

export function getSessionId(): string {
  let id = sessionStorage.getItem(SESSION_KEY);
  if (!id) {
    id = `sess_${Date.now()}_${Math.random().toString(36).slice(2, 9)}`;
    sessionStorage.setItem(SESSION_KEY, id);
  }
  return id;
}

export async function discoverOpportunities(
  query: string,
  language: 'en' | 'hi' = 'en'
): Promise<DiscoverResponse> {
  const res = await fetch(`${API_BASE}/discover`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ query, language, session_id: getSessionId() }),
  });
  if (!res.ok) {
    throw new Error(`API error: ${res.status}`);
  }
  return res.json();
}

export async function checkHealth(): Promise<Record<string, unknown>> {
  const res = await fetch(`${API_BASE}/health`);
  if (!res.ok) throw new Error(`Health check failed: ${res.status}`);
  return res.json();
}
