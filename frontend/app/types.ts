// Canonical AI Output Schema (v1) — mirrors ai-service/docs/api_contract.md.

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

// Each category is scored out of 20 (sum = overall_score, 0-100).
export const CATEGORY_MAX = 20;

export const CATEGORY_LABELS: Record<keyof CategoryScores, string> = {
  structure: "Structure",
  skills: "Skills",
  experience: "Experience",
  projects: "Projects",
  ats: "ATS"
};
