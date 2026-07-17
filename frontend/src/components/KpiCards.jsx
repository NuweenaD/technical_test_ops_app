import React from "react";
import { rm, pct } from "../format.js";

export default function KpiCards({ summary }) {
  const cards = [
    { label: "Total Net Revenue", value: rm(summary.total_revenue) },
    { label: "Orders", value: summary.order_count },
    { label: "Avg Order Value", value: rm(summary.avg_order_value) },
    { label: "Target Attainment", value: pct(summary.attainment_pct) },
  ];

  return (
    <div className="kpi-row">
      {cards.map((c) => (
        <div className="kpi-card" key={c.label}>
          <div className="kpi-value">{c.value}</div>
          <div className="kpi-label">{c.label}</div>
        </div>
      ))}
    </div>
  );
}
