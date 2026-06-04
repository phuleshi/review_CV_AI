/**
 * Canonical AI Output Schema (v1) — mirrors ai-service/docs/api_contract.md.
 * The backend proxies this through unchanged from the AI service to the frontend.
 */
export interface CategoryScores {
  structure: number;
  skills: number;
  experience: number;
  projects: number;
  ats: number;
}

export interface JdMatch {
  match_score: number;
  matched_skills: string[];
  missing_skills: string[];
  notes: string;
}

export interface ReviewResult {
  schema_version: string;
  overall_score: number;
  category_scores: CategoryScores;
  strengths: string[];
  weaknesses: string[];
  suggestions: string[];
  summary: string;
  jd_match: JdMatch | null;
}
