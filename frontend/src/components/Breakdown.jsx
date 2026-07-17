import React from "react";
import { rm } from "../format.js";

export default function Breakdown({ title, rows, labelKey }) {
  const max = Math.max(1, ...rows.map((r) => r.revenue));

  return (
    <div className="panel">
      <h2>{title}</h2>
      {rows.length === 0 && <p className="muted">No data.</p>}
      {rows.map((r) => (
        <div className="bar-row" key={r[labelKey]}>
          <div className="bar-label">{r[labelKey]}</div>
          <div className="bar-track">
            <div className="bar-fill" style={{ width: `${(r.revenue / max) * 100}%` }} />
          </div>
          <div className="bar-value">{rm(r.revenue)}</div>
        </div>
      ))}
    </div>
  );
}
