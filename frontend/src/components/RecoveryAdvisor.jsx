import React from "react";
import { rm } from "../format.js";

function displayMoney(value) {
  return value == null
    ? "N/A"
    : rm(value);
}

function displayNumber(value) {
  return value == null
    ? "N/A"
    : value;
}

function statusLabel(status) {
  const labels = {
    at_risk: "At Risk",
    on_track: "On Track",
    target_reached: "Target Reached",
    planning: "Planning",
    no_target: "No Target",
    completed_on_target:
      "Completed Above Target",
    completed_below_target:
      "Completed Below Target",
  };

  return labels[status] || status;
}

export default function RecoveryAdvisor({
  data,
}) {
  if (!data) {
    return null;
  }

  return (
    <div className="panel advisor-panel">
      <div className="advisor-header">
        <div>
          <h2>
            Revenue Recovery Advisor
          </h2>

          <p className="advisor-subtitle">
            Actionable plan based on the
            selected month&apos;s current
            sales performance
          </p>
        </div>

        <span
          className={
            `advisor-status advisor-${data.status}`
          }
        >
          {statusLabel(data.status)}
        </span>
      </div>

      <div className="advisor-message">
        {data.message}
      </div>

      <div className="advisor-grid">
        <div className="advisor-item">
          <div className="advisor-label">
            Revenue gap
          </div>

          <div className="advisor-value">
            {displayMoney(
              data.revenue_gap
            )}
          </div>
        </div>

        <div className="advisor-item">
          <div className="advisor-label">
            Days remaining
          </div>

          <div className="advisor-value">
            {displayNumber(
              data.days_remaining
            )}
          </div>
        </div>

        <div className="advisor-item">
          <div className="advisor-label">
            Required revenue per day
          </div>

          <div className="advisor-value">
            {displayMoney(
              data.required_daily_revenue
            )}
          </div>
        </div>

        <div className="advisor-item">
          <div className="advisor-label">
            Additional orders required
          </div>

          <div className="advisor-value">
            {displayNumber(
              data.additional_orders_required
            )}
          </div>
        </div>

        <div className="advisor-item">
          <div className="advisor-label">
            Required orders per day
          </div>

          <div className="advisor-value">
            {displayNumber(
              data.required_orders_per_day
            )}
          </div>
        </div>

        <div className="advisor-item">
          <div className="advisor-label">
            Current average order value
          </div>

          <div className="advisor-value">
            {displayMoney(
              data.current_aov
            )}
          </div>
        </div>
      </div>

      <div className="advisor-drivers">
        <div className="advisor-driver">
          <div className="advisor-label">
            Strongest category
          </div>

          <div className="advisor-driver-value">
            {data.top_category
              ? (
                <>
                  {data.top_category.name}
                  {" · "}
                  {rm(
                    data.top_category.revenue
                  )}
                </>
              )
              : "N/A"}
          </div>
        </div>

        <div className="advisor-driver">
          <div className="advisor-label">
            Strongest channel
          </div>

          <div className="advisor-driver-value">
            {data.top_channel
              ? (
                <>
                  {data.top_channel.name}
                  {" · "}
                  {rm(
                    data.top_channel.revenue
                  )}
                </>
              )
              : "N/A"}
          </div>
        </div>
      </div>
    </div>
  );
}