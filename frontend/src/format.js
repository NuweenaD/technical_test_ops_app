export const rm = (n) =>
  n == null
    ? "—"
    : "RM " +
      Number(n).toLocaleString("en-MY", {
        minimumFractionDigits: 2,
        maximumFractionDigits: 2,
      });

export const pct = (n) =>
  n == null ? "—" : Number(n).toLocaleString("en-MY", { maximumFractionDigits: 1 }) + "%";
