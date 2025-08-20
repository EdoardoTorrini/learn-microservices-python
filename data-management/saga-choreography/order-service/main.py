import asyncio
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from shared.messaging import EventBus
from shared.events import new_event
from shared.settings import settings
from .db import engine, SessionLocal, Base
from .schemas import CreateOrderRequest, OrderRead, OrderStatus
from .repository import create_order, get_order, set_status, has_processed, mark_processed

app = FastAPI(title="Order Service")
bus = EventBus()

async def get_db():
    async with SessionLocal() as session:
        yield session

@app.on_event("startup")
async def startup():
    # DB init
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    # Nessun seed necessario per orders
    # MQ
    await bus.connect()
    if not settings.DISABLE_MQ:
        asyncio.create_task(bus.subscribe("payment.failed", on_payment_failed))
        asyncio.create_task(bus.subscribe("inventory.ok", on_inventory_ok))
        asyncio.create_task(bus.subscribe("inventory.failed", on_inventory_failed))

async def on_payment_failed(evt: dict):
    async with SessionLocal() as db:
        if await has_processed(db, evt["event_id"]): return
        oid = evt["correlation_id"]
        await set_status(db, oid, OrderStatus.CANCELLED)
        await mark_processed(db, evt["event_id"])

async def on_inventory_ok(evt: dict):
    async with SessionLocal() as db:
        if await has_processed(db, evt["event_id"]): return
        oid = evt["correlation_id"]
        await set_status(db, oid, OrderStatus.CONFIRMED)
        await mark_processed(db, evt["event_id"])

async def on_inventory_failed(evt: dict):
    async with SessionLocal() as db:
        if await has_processed(db, evt["event_id"]): return
        oid = evt["correlation_id"]
        await set_status(db, oid, OrderStatus.CANCELLED)
        await mark_processed(db, evt["event_id"])

@app.post("/order", response_model=dict)
async def create(req: CreateOrderRequest, db: AsyncSession = Depends(get_db)):
    order = await create_order(
        db,
        customer_id=req.customer_id,
        items=[i.model_dump() for i in req.items],
        amount=req.total_amount,
    )
    # includo l'intero ordine nel payload così i consumer hanno tutto
    evt = new_event(
        "order.created",
        correlation_id=order.id,
        payload={
            "order_id": order.id,
            "customer_id": order.customer_id,
            "items": [i.model_dump() for i in req.items],
            "total_amount": req.total_amount,
        },
    )
    await bus.publish("order.created", evt.model_dump())
    return {"order_id": order.id, "status": order.status.value}

@app.get("/order/{order_id}", response_model=OrderRead)
async def read(order_id: str, db: AsyncSession = Depends(get_db)):
    order = await get_order(db, order_id)
    if not order:
        raise HTTPException(404, "Order not found")
    return OrderRead(
        id=order.id,
        status=order.status.value,
        customer_id=order.customer_id,
        items=[{"sku": it.sku, "qty": it.qty} for it in order.items],
        total_amount=order.total_amount,
    )

@app.get("/health")
async def health():
    try:
        async with engine.begin() as conn:
            await conn.execute(text("SELECT 1"))
        return {"status": "ok"}
    except Exception as e:
        return {"status": "error", "detail": str(e)}
