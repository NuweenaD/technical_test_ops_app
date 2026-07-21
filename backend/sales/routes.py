"""HTTP routes for the Sales KPI Dashboard.

Thin handlers — they acquire a connection and delegate to `db`. The KPI math
lives in `db.summary()` / `db.pace_to_target()`.
"""

from datetime import date

from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel

import db

router = APIRouter()


class SaleIn(BaseModel):
    sale_date: date
    product: str
    category: str
    channel: str
    quantity: int
    unit_price: float
    discount_pct: float = 0
    status: str = "completed"


@router.get("/summary")
async def get_summary(month: str | None = None, category: str | None = None, channel: str | None = None):
    async with db.pool.acquire() as conn:
        return await db.summary(conn, month, category, channel)


@router.get("/sales")
async def get_sales(month: str | None = None, category: str | None = None, channel: str | None = None):
    async with db.pool.acquire() as conn:
        return await db.list_sales(conn, month, category, channel)


@router.post("/sales")
async def post_sale(sale: SaleIn):
    async with db.pool.acquire() as conn:
        return await db.create_sale(conn, sale.model_dump())


@router.delete("/sales/{sale_id}")
async def remove_sale(sale_id: int):
    async with db.pool.acquire() as conn:
        await db.delete_sale(conn, sale_id)
    return {"ok": True}


@router.get("/filters")
async def get_filters():
    async with db.pool.acquire() as conn:
        return await db.filters(conn)


@router.get("/targets")
async def get_targets():
    async with db.pool.acquire() as conn:
        return await db.list_targets(conn)


@router.get("/pace-to-target")
async def get_pace_to_target(month: str = Query(..., pattern=r"^\d{4}-\d{2}$")):
    try:
        async with db.pool.acquire() as conn:
            return await db.pace_to_target(conn, month)
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc

@router.get("/recovery-advisor")
async def get_recovery_advisor(
    month: str = Query(
        ...,
        pattern=r"^\d{4}-\d{2}$",
    ),
):
    try:
        async with db.pool.acquire() as conn:
            return await db.recovery_advisor(
                conn,
                month,
            )
    except ValueError as exc:
        raise HTTPException(
            status_code=422,
            detail=str(exc),
        ) from exc