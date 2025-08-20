import uuid
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from .models import Order, OrderItem, OrderStatus, ProcessedEvent

async def create_order(db: AsyncSession, customer_id: str, items: list[dict], amount: float) -> Order:
    oid = str(uuid.uuid4())
    order = Order(id=oid, status=OrderStatus.PENDING, customer_id=customer_id, total_amount=amount)
    order.items = [OrderItem(sku=i["sku"], qty=i["qty"]) for i in items]
    db.add(order)
    await db.commit()
    await db.refresh(order)
    return order

async def get_order(db: AsyncSession, oid: str) -> Order | None:
    res = await db.execute(select(Order).where(Order.id == oid))
    return res.scalar_one_or_none()

async def set_status(db: AsyncSession, oid: str, status: OrderStatus):
    await db.execute(update(Order).where(Order.id == oid).values(status=status))
    await db.commit()

async def has_processed(db: AsyncSession, event_id: str) -> bool:
    res = await db.execute(select(ProcessedEvent).where(ProcessedEvent.event_id == event_id))
    return res.scalar_one_or_none() is not None

async def mark_processed(db: AsyncSession, event_id: str):
    db.add(ProcessedEvent(event_id=event_id))
    await db.commit()
