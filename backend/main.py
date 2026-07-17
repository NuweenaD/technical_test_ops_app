"""Sales KPI Dashboard — FastAPI entrypoint.

Wires shared setup (CORS, DB lifecycle) and mounts the sales router. Business
logic and the DB schema live in `db.py`; HTTP routes live in `sales/routes.py`.
"""

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

import db
from sales.routes import router as sales_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Create the pool, ensure the schema, and seed sample data on first boot.
    await db.init_db()
    yield
    await db.close_db()


app = FastAPI(title="Sales KPI Dashboard", lifespan=lifespan)

# Open CORS — this is a local test harness, not a production service.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(sales_router, prefix="/api")


@app.get("/api/health")
async def health():
    return {"ok": True}
