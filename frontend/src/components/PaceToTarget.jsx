import React from "react";
import { rm, pct } from "../format.js";

export default function PaceToTarget({ data }) {
  if (!data) return null;

  let paceDisplay;
  if (data.status === "not_started") {
    paceDisplay = <span className="muted">N/A — month has not started</span>;
  } else if (data.status === "no_target") {
    paceDisplay = <span className="muted">N/A — no target set</span>;
  } else {
    const sign = data.pace_vs_target_rm >= 0 ? "+" : "";
    paceDisplay = (
      <span className={data.status === "on_track" ? "pace-on-track" : "pace-at-risk"}>
        {sign}
        {rm(data.pace_vs_target_rm)} ({sign}
        {pct(data.pace_vs_target_pct)}) —{" "}
        <strong>{data.status === "on_track" ? "On Track" : "At Risk"}</strong>
      </span>
    );
  }

  return (
    <div className="panel">
      <h2>Pace to Target</h2>

      <div className="pace-grid">
        <div className="pace-item">
          <div className="pace-label">Month-to-date revenue</div>
          <div className="pace-value">{rm(data.month_to_date_revenue)}</div>
        </div>
        <div className="pace-item">
          <div className="pace-label">Days elapsed</div>
          <div className="pace-value">
            {data.days_elapsed} / {data.days_in_month}
          </div>
        </div>
        <div className="pace-item">
          <div className="pace-label">Projected month-end revenue</div>
          <div className="pace-value">{rm(data.projected_revenue)}</div>
        </div>
        <div className="pace-item">
          <div className="pace-label">Monthly target</div>
          <div className="pace-value">{rm(data.target)}</div>
        </div>
      </div>

      {/* Labelled "pace variance" (not "attainment") since this is
          (projected - target) / target — a different metric from the
          Target Attainment % shown in KpiCards (total_revenue / target). */}
      <div className="pace-summary">
        <div className="pace-label">Pace variance vs target</div>
        <div className="pace-summary-value">{paceDisplay}</div>
      </div>
    </div>
  );
}
