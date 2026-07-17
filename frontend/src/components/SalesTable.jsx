import React from "react";
import * as api from "../api.js";
import { rm } from "../format.js";

export default function SalesTable({ sales, onDeleted }) {
  const remove = async (id) => {
    if (!confirm("Delete this sale?")) return;
    await api.deleteSale(id);
    onDeleted();
  };

  return (
    <div className="panel">
      <h2>Sales ({sales.length})</h2>
      <div className="table-wrap">
        <table>
          <thead>
            <tr>
              <th>Date</th>
              <th>Product</th>
              <th>Category</th>
              <th>Channel</th>
              <th className="num">Qty</th>
              <th className="num">Unit</th>
              <th className="num">Disc %</th>
              <th>Status</th>
              <th></th>
            </tr>
          </thead>
          <tbody>
            {sales.map((s) => (
              <tr key={s.id} className={s.status === "refunded" ? "refunded" : ""}>
                <td>{s.sale_date}</td>
                <td>{s.product}</td>
                <td>{s.category}</td>
                <td>{s.channel}</td>
                <td className="num">{s.quantity}</td>
                <td className="num">{rm(s.unit_price)}</td>
                <td className="num">{s.discount_pct}</td>
                <td>
                  <span className={`badge ${s.status}`}>{s.status}</span>
                </td>
                <td>
                  <button className="link-btn" onClick={() => remove(s.id)}>
                    Delete
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
