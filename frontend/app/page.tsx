"use client";

import { useMemo, useState } from "react";

const defaultCvText = `Frontend Developer
3 years experience building web apps with Next.js, React, and TypeScript.
Worked on dashboards, internal tools, and CV screening flows.`;

export default function HomePage() {
  const [cvText, setCvText] = useState(defaultCvText);
  const [jobText, setJobText] = useState(
    "Looking for a frontend engineer with Next.js, TypeScript, UI polish, and strong communication."
  );

  const score = useMemo(() => {
    const cv = cvText.toLowerCase();
    const job = jobText.toLowerCase();
    const keywords = ["next.js", "react", "typescript", "ui", "frontend"];
    const matched = keywords.filter((keyword) => cv.includes(keyword) && job.includes(keyword));
    return Math.min(100, 40 + matched.length * 12 + Math.min(cvText.length / 20, 20));
  }, [cvText, jobText]);

  const strengths = [
    "Có kinh nghiệm frontend thực chiến.",
    "Có đề cập đến Next.js và TypeScript.",
    "Dễ triển khai thành luồng review thật sau này."
  ];

  const improvements = [
    "Thêm số liệu cụ thể cho từng dự án.",
    "Bổ sung kinh nghiệm AI / parsing CV nếu có.",
    "Chia rõ sections: Summary, Skills, Experience."
  ];

  return (
    <main className="page">
      <section className="hero">
        <p className="eyebrow">AI CV Review Platform</p>
        <h1>Giao diện test local cực đơn giản</h1>
        <p className="subtitle">
          Màn hình này chỉ để kiểm tra layout và flow ban đầu. Chưa nối backend, chưa gọi database.
        </p>
      </section>

      <section className="grid">
        <div className="card">
          <h2>CV text</h2>
          <textarea
            value={cvText}
            onChange={(event) => setCvText(event.target.value)}
            placeholder="Paste CV here..."
            rows={10}
          />
          <label className="file">
            <span>Hoặc chọn file PDF/DOCX sau này</span>
            <input type="file" disabled />
          </label>
        </div>

        <div className="card">
          <h2>Job description</h2>
          <textarea
            value={jobText}
            onChange={(event) => setJobText(event.target.value)}
            placeholder="Paste job description here..."
            rows={10}
          />
          <button type="button">Test review</button>
        </div>
      </section>

      <section className="result">
        <div className="scoreCard">
          <span>Compatibility score</span>
          <strong>{Math.round(score)}%</strong>
          <p>Điểm demo được tính cục bộ từ nội dung nhập vào.</p>
        </div>

        <div className="listCard">
          <h3>Strengths</h3>
          <ul>
            {strengths.map((item) => (
              <li key={item}>{item}</li>
            ))}
          </ul>
        </div>

        <div className="listCard">
          <h3>Improvements</h3>
          <ul>
            {improvements.map((item) => (
              <li key={item}>{item}</li>
            ))}
          </ul>
        </div>
      </section>
    </main>
  );
}
