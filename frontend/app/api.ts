import type { ReviewResult } from "./types";

const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL ?? "http://localhost:4000/api";

export async function reviewCv(
  cvText: string,
  jobDescription?: string
): Promise<ReviewResult> {
  const res = await fetch(`${API_BASE_URL}/review-cv`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      cv_text: cvText,
      job_description: jobDescription?.trim() ? jobDescription : null
    })
  });

  if (!res.ok) {
    let detail = `Request failed (${res.status})`;
    try {
      const body = await res.clone().json();
      if (body?.message) detail = Array.isArray(body.message) ? body.message.join(", ") : body.message;
      if (body?.detail) detail = typeof body.detail === "string" ? body.detail : JSON.stringify(body.detail);
    } catch {
      const text = await res.text().catch(() => "");
      if (text) detail = text;
    }
    throw new Error(detail);
  }

  return (await res.json()) as ReviewResult;
}
