"use client";

import { useState } from "react";
import { reviewCv } from "./api";
import { CATEGORY_LABELS, CATEGORY_MAX, type CategoryScores, type ReviewResult } from "./types";

const defaultCvText = `Frontend Developer
3 years experience building web apps with Next.js, React, and TypeScript.
Worked on dashboards, internal tools, and CV screening flows.
- Reduced page load time by 35% via code-splitting.
Projects: github.com/example/portfolio`;

const defaultJobText =
  "Looking for a frontend engineer with Next.js, TypeScript, UI polish, and strong communication.";

function scoreColor(ratio: number): string {
  if (ratio >= 0.8) return "#16a34a";
  if (ratio >= 0.5) return "#d97706";
  return "#dc2626";
}

export default function HomePage() {
  const [cvText, setCvText] = useState(defaultCvText);
  const [jobText, setJobText] = useState(defaultJobText);
  const [result, setResult] = useState<ReviewResult | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  async function handleReview() {
    if (!cvText.trim()) {
      setError("Vui lòng nhập nội dung CV.");
      return;
    }
    setLoading(true);
    setError(null);
    try {
      setResult(await reviewCv(cvText, jobText));
    } catch (err) {
      setError(err instanceof Error ? err.message : "Đã có lỗi xảy ra.");
      setResult(null);
    } finally {
      setLoading(false);
    }
  }

  return (
    <main className="page">
      <section className="hero">
        <p className="eyebrow">AI CV Review Platform</p>
        <h1>CV Review</h1>
        <p className="subtitle">
          Nhập CV (và JD tuỳ chọn), hệ thống gọi Backend → AI Service và trả về điểm theo
          schema chuẩn: 5 tiêu chí (mỗi tiêu chí /20) cộng lại thành điểm tổng /100.
        </p>
      </section>

      <section className="grid">
        <div className="card">
          <h2>CV text</h2>
          <textarea
            value={cvText}
            onChange={(event) => setCvText(event.target.value)}
            placeholder="Paste CV here..."
            rows={12}
          />
          <label className="file">
            <span>Hoặc chọn file PDF/DOCX (sẽ hỗ trợ sau)</span>
            <input type="file" disabled />
          </label>
        </div>

        <div className="card">
          <h2>Job description (tuỳ chọn)</h2>
          <textarea
            value={jobText}
            onChange={(event) => setJobText(event.target.value)}
            placeholder="Paste job description here..."
            rows={12}
          />
          <button type="button" onClick={handleReview} disabled={loading}>
            {loading ? "Đang chấm..." : "Review CV"}
          </button>
        </div>
      </section>

      {error && <p className="error">⚠️ {error}</p>}

      {result && (
        <>
          <section className="result">
            <div className="scoreCard">
              <span>Overall score</span>
              <strong style={{ color: scoreColor(result.overall_score / 100) }}>
                {result.overall_score}
                <small>/100</small>
              </strong>
              <p>{result.summary}</p>
            </div>

            <div className="card">
              <h3>Category scores</h3>
              <div className="categories">
                {(Object.keys(CATEGORY_LABELS) as (keyof CategoryScores)[]).map((key) => {
                  const value = result.category_scores[key];
                  const ratio = value / CATEGORY_MAX;
                  return (
                    <div className="categoryRow" key={key}>
                      <div className="categoryHead">
                        <span>{CATEGORY_LABELS[key]}</span>
                        <strong>
                          {value}/{CATEGORY_MAX}
                        </strong>
                      </div>
                      <div className="bar">
                        <div
                          className="barFill"
                          style={{ width: `${ratio * 100}%`, background: scoreColor(ratio) }}
                        />
                      </div>
                    </div>
                  );
                })}
              </div>
            </div>
          </section>

          <section className="lists">
            <div className="listCard">
              <h3>✅ Strengths</h3>
              <ul>
                {result.strengths.map((item, i) => (
                  <li key={i}>{item}</li>
                ))}
              </ul>
            </div>
            <div className="listCard">
              <h3>⚠️ Weaknesses</h3>
              <ul>
                {result.weaknesses.map((item, i) => (
                  <li key={i}>{item}</li>
                ))}
              </ul>
            </div>
            <div className="listCard">
              <h3>💡 Suggestions</h3>
              <ul>
                {result.suggestions.map((item, i) => (
                  <li key={i}>{item}</li>
                ))}
              </ul>
            </div>
          </section>
        </>
      )}
    </main>
  );
}
