"""Database layer — connection pool, schema, seed data, and all queries.

Follows the app's convention of keeping schema + queries together with no
migration framework: `init_db()` creates the tables at startup and seeds
sample data the first time the database is empty.

The dashboard KPIs are computed in `summary()`.
"""

import os
from datetime import date, timedelta
from decimal import Decimal

import asyncpg

DATABASE_URL = os.getenv(
    "DATABASE_URL", "postgresql://sales:sales@localhost:5442/sales"
)

# Shared connection pool, set by init_db().
pool: asyncpg.Pool | None = None

SCHEMA_SQL = """
CREATE TABLE IF NOT EXISTS sales (
    id           SERIAL PRIMARY KEY,
    sale_date    DATE          NOT NULL,
    product      TEXT          NOT NULL,
    category     TEXT          NOT NULL,
    channel      TEXT          NOT NULL,          -- 'online' | 'in_store'
    quantity     INTEGER       NOT NULL,
    unit_price   NUMERIC(10,2) NOT NULL,
    discount_pct NUMERIC(5,2)  NOT NULL DEFAULT 0,
    status       TEXT          NOT NULL DEFAULT 'completed',  -- 'completed' | 'refunded'
    created_at   TIMESTAMPTZ   NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS monthly_targets (
    id            SERIAL PRIMARY KEY,
    month         TEXT          NOT NULL UNIQUE,   -- 'YYYY-MM'
    target_amount NUMERIC(12,2) NOT NULL
);
"""


async def init_db():
    global pool
    pool = await asyncpg.create_pool(DATABASE_URL, min_size=1, max_size=10)
    async with pool.acquire() as conn:
        await conn.execute(SCHEMA_SQL)
        await seed_if_empty(conn)


async def close_db():
    if pool is not None:
        await pool.close()


# --------------------------------------------------------------------------- #
# Revenue helper
# --------------------------------------------------------------------------- #
def _line_net(r):
    """Return net revenue for a single completed sale line."""
    gross_revenue = r["quantity"] * r["unit_price"]
    discount_rate = r["discount_pct"] / Decimal("100")
    return float(gross_revenue * (Decimal("1") - discount_rate))

# --------------------------------------------------------------------------- #
# Filters
# --------------------------------------------------------------------------- #

def _build_filters(month, category, channel):
    """Return (where_sql, params) for the shared sales filters."""
    clauses, params = [], []
    if month:
        params.append(month)
        clauses.append(f"to_char(sale_date, 'YYYY-MM') = ${len(params)}")
    if category:
        params.append(category)
        clauses.append(f"category = ${len(params)}")
    if channel:
        params.append(channel)
        clauses.append(f"channel = ${len(params)}")
    where = ("WHERE " + " AND ".join(clauses)) if clauses else ""
    return where, params


# --------------------------------------------------------------------------- #
# Summary KPIs
# --------------------------------------------------------------------------- #

#Gantikan overall function summary - discount treated as fixed RM, Refunded sales included, Category revenue overwritten, online classified as in-store, target attainment incorrect
async def summary(conn, month=None, category=None, channel=None):
    where, params = _build_filters(month, category, channel)
    rows = await conn.fetch(f"SELECT * FROM sales {where}", *params)

    # FIX: Penapis jualan yang completed sahaja (elak refunded / cancelled sales dimasukkan sekali)
    # KPI calculations should only include completed sales.
    completed_rows = [r for r in rows if r["status"] == "completed"]

    # Totals
    # FIX: _line_net(r) digunakan untuk pastikan discount difahami sebagai percentage (bukan fixed RM sahaja)
    total_revenue = sum(_line_net(r) for r in completed_rows)
    order_count = len(completed_rows)
    aov = total_revenue / order_count if order_count else 0.0

    # Revenue by category
    by_category = {}
    for r in completed_rows:
        category_name = r["category"]
        # FIX: Tambah hasil jualan terkini pada amount sedia ada (elak nilai kategori ter-overwritten)
        by_category[category_name] = (
            by_category.get(category_name, 0.0) + _line_net(r)
        )

    # Revenue by channel
    by_channel = {"online": 0.0, "in_store": 0.0}
    for r in completed_rows:
        channel_name = r["channel"]
        # FIX: Match follows kunci saluran yang tepat (avoid online classifies as in_store)
        if channel_name in by_channel:
            by_channel[channel_name] += _line_net(r)

    # Target attainment for the selected month
    target = None
    if month:
        target = await conn.fetchval(
            "SELECT target_amount FROM monthly_targets WHERE month = $1",
            month,
        )

    target_value = float(target) if target is not None else None
    # FIX: Kira pencapaian sasaran (%) dengan membahagikan total_revenue with target_value correctly
    attainment_pct = (
        round(total_revenue / target_value * 100, 1)
        if target_value is not None and target_value > 0
        else None
    )

    return {
        "total_revenue": round(total_revenue, 2),
        "order_count": order_count,
        "avg_order_value": round(aov, 2),
        "target": target_value,
        "attainment_pct": attainment_pct,
        "by_category": [
            {"category": key, "revenue": round(value, 2)}
            for key, value in sorted(by_category.items())
        ],
        "by_channel": [
            {"channel": key, "revenue": round(value, 2)}
            for key, value in by_channel.items()
        ],
    }


# --------------------------------------------------------------------------- #
# Sales CRUD
# --------------------------------------------------------------------------- #

async def list_sales(conn, month=None, category=None, channel=None):
    where, params = _build_filters(month, category, channel)
    rows = await conn.fetch(
        f"SELECT * FROM sales {where} ORDER BY sale_date DESC, id DESC", *params
    )
    return [dict(r) for r in rows]


async def create_sale(conn, s):
    row = await conn.fetchrow(
        "INSERT INTO sales (sale_date, product, category, channel, quantity,"
        " unit_price, discount_pct, status)"
        " VALUES ($1,$2,$3,$4,$5,$6,$7,$8) RETURNING *",
        s["sale_date"],
        s["product"],
        s["category"],
        s["channel"],
        int(s["quantity"]),
        Decimal(str(s["unit_price"])),
        Decimal(str(s.get("discount_pct") or 0)),
        s.get("status") or "completed",
    )
    return dict(row)


async def delete_sale(conn, sale_id):
    await conn.execute("DELETE FROM sales WHERE id = $1", sale_id)


async def filters(conn):
    cats = await conn.fetch("SELECT DISTINCT category FROM sales ORDER BY category")
    chans = await conn.fetch("SELECT DISTINCT channel FROM sales ORDER BY channel")
    months = await conn.fetch(
        "SELECT DISTINCT to_char(sale_date, 'YYYY-MM') AS m FROM sales ORDER BY m DESC"
    )
    return {
        "categories": [r["category"] for r in cats],
        "channels": [r["channel"] for r in chans],
        "months": [r["m"] for r in months],
    }


async def list_targets(conn):
    rows = await conn.fetch(
        "SELECT month, target_amount FROM monthly_targets ORDER BY month DESC"
    )
    return [{"month": r["month"], "target_amount": float(r["target_amount"])} for r in rows]


# --------------------------------------------------------------------------- #
# Seed data (first boot only) — dated relative to today so the current month is
# always partially elapsed and the pacing feature stays demonstrable.
# --------------------------------------------------------------------------- #

def _month_str(d: date, back: int) -> str:
    y, m = d.year, d.month - back
    while m <= 0:
        m += 12
        y -= 1
    return f"{y}-{m:02d}"


async def seed_if_empty(conn):
    n = await conn.fetchval("SELECT COUNT(*) FROM sales")
    if n and n > 0:
        return

    today = date.today()
    categories = [
        ("Cafe", ["Latte", "Iced Tea", "Sandwich", "Protein Bar"]),
        ("Pro Shop", ["Paddle", "Grip Tape", "Ball Pack", "Cap"]),
        ("Coaching", ["Private Lesson", "Group Clinic"]),
        ("Court Booking", ["Peak Hour", "Off-Peak Hour"]),
    ]
    channels = ["online", "in_store"]
    prices = [15, 20, 28, 35, 45, 60, 85, 120]
    discounts = [0, 0, 0, 0, 10, 15, 20]

    rows = []
    for d in range(75):  # today back to 74 days ago
        day = today - timedelta(days=d)
        count = 1 + ((d * 3 + 1) % 3)  # 1..3 sales per day
        for i in range(count):
            k = d + i
            cat, products = categories[k % len(categories)]
            product = products[(k // 2) % len(products)]
            channel = channels[k % 2]
            quantity = 1 + (k % 4)
            unit_price = prices[k % len(prices)]
            discount = discounts[k % len(discounts)]
            status = "refunded" if (k % 13 == 0) else "completed"
            rows.append(
                (day, product, cat, channel, quantity, Decimal(unit_price), Decimal(discount), status)
            )

    await conn.executemany(
        "INSERT INTO sales (sale_date, product, category, channel, quantity,"
        " unit_price, discount_pct, status) VALUES ($1,$2,$3,$4,$5,$6,$7,$8)",
        rows,
    )

    for back in range(3):
        await conn.execute(
            "INSERT INTO monthly_targets (month, target_amount) VALUES ($1, $2)"
            " ON CONFLICT (month) DO NOTHING",
            _month_str(today, back),
            Decimal(10000),
        )
