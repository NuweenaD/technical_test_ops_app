import React from "react";

export default function FilterBar({ filters, options, onChange }) {
  const set = (key) => (e) => onChange({ ...filters, [key]: e.target.value });

  return (
    <div className="filter-bar">
      <label>
        Month
        <select value={filters.month} onChange={set("month")}>
          <option value="">All months</option>
          {options.months.map((m) => (
            <option key={m} value={m}>
              {m}
            </option>
          ))}
        </select>
      </label>

      <label>
        Category
        <select value={filters.category} onChange={set("category")}>
          <option value="">All categories</option>
          {options.categories.map((c) => (
            <option key={c} value={c}>
              {c}
            </option>
          ))}
        </select>
      </label>

      <label>
        Channel
        <select value={filters.channel} onChange={set("channel")}>
          <option value="">All channels</option>
          {options.channels.map((c) => (
            <option key={c} value={c}>
              {c}
            </option>
          ))}
        </select>
      </label>
    </div>
  );
}
