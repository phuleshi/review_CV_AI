"use client";

import { useState, useEffect } from "react";
import { reviewCv, getHistory } from "./api";
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
  const [history, setHistory] = useState<any[]>([]);
  const [activeHistoryId, setActiveHistoryId] = useState<string | null>(null);

  // Fetch history on mount
  useEffect(() => {
    async function loadHistory() {
      try {
        const data = await getHistory();
        setHistory(data);
      } catch (err) {
        console.error("Failed to load history:", err);
      }
    }
    loadHistory();
  }, []);

  async function handleReview() {
    if (!cvText.trim()) {
      setError("Vui lòng nhập nội dung CV.");
      return;
    }
    setLoading(true);
    setError(null);
    try {
      const response = await reviewCv(cvText, jobText);
      setResult(response);
      
      // Reload history to get latest list with correct DB values
      const data = await getHistory();
      setHistory(data);
      if (data.length > 0) {
        setActiveHistoryId(data[0].id);
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : "Đã có lỗi xảy ra.");
      setResult(null);
    } finally {
      setLoading(false);
    }
  }

  function handleSelectHistoryItem(item: any) {
    setActiveHistoryId(item.id);
    setCvText(item.cv_text || "");
    setJobText(item.job_description || "");
    setResult({
      overall_score: item.overall_score,
      category_scores: item.category_scores,
      strengths: item.strengths,
      weaknesses: item.weaknesses,
      suggestions: item.suggestions,
      summary: item.summary,
      jd_match: item.jd_match,
      schema_version: "1.0"
    });
  }

  function getFirstLine(text: string): string {
    const line = text.trim().split("\n")[0];
    return line || "CV không có tiêu đề";
  }

  return (
    <div className="app-layout">
      {/* Sidebar for History */}
      <aside className="sidebar">
        <h2>Lịch sử đánh giá</h2>
        <div className="history-list">
          {history.length === 0 ? (
            <p style={{ color: "var(--muted)", fontSize: "14px", textAlign: "center" }}>
              Chưa có lịch sử đánh giá
            </p>
          ) : (
            history.map((item) => {
              const ratio = item.overall_score / 100;
              const dateStr = item.createdAt
                ? new Date(item.createdAt).toLocaleDateString("vi-VN", {
                    hour: "2-digit",
                    minute: "2-digit"
                  })
                : "Không rõ thời gian";
              return (
                <button
                  type="button"
                  key={item.id}
                  onClick={() => handleSelectHistoryItem(item)}
                  className={`history-item ${activeHistoryId === item.id ? "active" : ""}`}
                >
                  <span className="title-snippet">{getFirstLine(item.cv_text)}</span>
                  <div className="score-badge">
                    <span
                      className="score-circle"
                      style={{ background: scoreColor(ratio) }}
                    />
                    <span>Điểm: {item.overall_score}/100</span>
                  </div>
                  <span className="meta">{dateStr}</span>
                </button>
              );
            })
          )}
        </div>
      </aside>

      {/* Main Page Content */}
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
              <h3>Strengths</h3>
              <ul>
                {result.strengths.map((item, i) => (
                  <li key={i}>{item}</li>
                ))}
              </ul>
            </div>
            <div className="listCard">
              <h3>Weaknesses</h3>
              <ul>
                {result.weaknesses.map((item, i) => (
                  <li key={i}>{item}</li>
                ))}
              </ul>
            </div>
            <div className="listCard">
              <h3>Suggestions</h3>
              <ul>
                {result.suggestions.map((item, i) => (
                  <li key={i}>{item}</li>
                ))}
              </ul>
            </div>
          </section>

          {result.jd_match && (
            <section className="jdMatch card">
              <div>
                <span className="sectionLabel">JD match</span>
                <strong style={{ color: scoreColor(result.jd_match.match_score / 100) }}>
                  {result.jd_match.match_score}
                  <small>/100</small>
                </strong>
                <p>{result.jd_match.notes}</p>
              </div>

              <div className="skillColumns">
                <div>
                  <h3>Matched skills</h3>
                  {result.jd_match.matched_skills.length ? (
                    <div className="pills">
                      {result.jd_match.matched_skills.map((skill) => (
                        <span className="pill positive" key={skill}>
                          {skill}
                        </span>
                      ))}
                    </div>
                  ) : (
                    <p className="muted">Chưa tìm thấy skill trùng với JD.</p>
                  )}
                </div>

                <div>
                  <h3>Missing skills</h3>
                  {result.jd_match.missing_skills.length ? (
                    <div className="pills">
                      {result.jd_match.missing_skills.map((skill) => (
                        <span className="pill warning" key={skill}>
                          {skill}
                        </span>
                      ))}
                    </div>
                  ) : (
                    <p className="muted">Không có skill thiếu nổi bật.</p>
                  )}
                </div>
              </div>
            </section>
          )}
        </>
      )}
    </main>
  );
}
