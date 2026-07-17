import React, { useState } from "react";
import * as api from "../api.js";

const today = () => {
  const d = new Date();
  return `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, "0")}-${String(
    d.getDate()
  ).padStart(2, "0")}`;
};

const empty = () => ({
  sale_date: today(),
  product: "",
  category: "",
  channel: "online",
  quantity: 1,
  unit_price: "",
  discount_pct: 0,
  status: "completed",
});

export default function AddSaleForm({ options, onCreated }) {
  const [form, setForm] = useState(empty());
  const [busy, setBusy] = useState(false);
  const set = (key) => (e) => setForm({ ...form, [key]: e.target.value });

  const submit = async (e) => {
    e.preventDefault();
    setBusy(true);
    try {
      await api.createSale({
        ...form,
        quantity: Number(form.quantity),
        unit_price: Number(form.unit_price),
        discount_pct: Number(form.discount_pct),
      });
      setForm(empty());
      onCreated();
    } catch (err) {
      alert("Failed to add sale: " + (err.message || err));
    } finally {
      setBusy(false);
    }
  };

  return (
    <form className="panel add-form" onSubmit={submit}>
      <h2>Add Sale</h2>
      <div className="form-grid">
        <label>
          Date
          <input type="date" value={form.sale_date} onChange={set("sale_date")} required />
        </label>
        <label>
          Product
          <input value={form.product} onChange={set("product")} required />
        </label>
        <label>
          Category
          <input value={form.category} onChange={set("category")} list="cat-list" required />
          <datalist id="cat-list">
            {options.categories.map((c) => (
              <option key={c} value={c} />
            ))}
          </datalist>
        </label>
        <label>
          Channel
          <select value={form.channel} onChange={set("channel")}>
            <option value="online">online</option>
            <option value="in_store">in_store</option>
          </select>
        </label>
        <label>
          Quantity
          <input type="number" min="1" value={form.quantity} onChange={set("quantity")} required />
        </label>
        <label>
          Unit Price (RM)
          <input
            type="number"
            step="0.01"
            min="0"
            value={form.unit_price}
            onChange={set("unit_price")}
            required
          />
        </label>
        <label>
          Discount %
          <input
            type="number"
            step="0.01"
            min="0"
            max="100"
            value={form.discount_pct}
            onChange={set("discount_pct")}
          />
        </label>
        <label>
          Status
          <select value={form.status} onChange={set("status")}>
            <option value="completed">completed</option>
            <option value="refunded">refunded</option>
          </select>
        </label>
      </div>
      <button type="submit" disabled={busy}>
        {busy ? "Adding…" : "Add Sale"}
      </button>
    </form>
  );
}
