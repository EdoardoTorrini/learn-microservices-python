import asyncio, json
import aio_pika
from .settings import settings

EXCHANGE_NAME = "saga"

class EventBus:
    def __init__(self):
        self._conn: aio_pika.RobustConnection | None = None
        self._channel: aio_pika.abc.AbstractChannel | None = None
        self._exchange: aio_pika.abc.AbstractExchange | None = None

    async def connect(self):
        if settings.DISABLE_MQ:
            return
        self._conn = await aio_pika.connect_robust(settings.RABBIT_URL)
        self._channel = await self._conn.channel()
        self._exchange = await self._channel.declare_exchange(
            EXCHANGE_NAME, aio_pika.ExchangeType.TOPIC, durable=True
        )

    async def publish(self, routing_key: str, message: dict):
        if settings.DISABLE_MQ:
            # nei test, non pubblichiamo
            return
        assert self._exchange is not None
        body = json.dumps(message).encode("utf-8")
        await self._exchange.publish(
            aio_pika.Message(
                body=body,
                content_type="application/json",
                delivery_mode=aio_pika.DeliveryMode.PERSISTENT,
            ),
            routing_key=routing_key,
        )

    async def subscribe(self, routing_key: str, handler):
        if settings.DISABLE_MQ:
            return
        assert self._channel is not None and self._exchange is not None
        queue = await self._channel.declare_queue(durable=True)
        await queue.bind(self._exchange, routing_key)
        async with queue.iterator() as qiter:
            async for message in qiter:
                async with message.process():
                    try:
                        payload = json.loads(message.body.decode("utf-8"))
                        await handler(payload)
                    except Exception as e:
                        # TODO: logging + DLQ
                        pass

    async def close(self):
        if self._conn:
            await self._conn.close()
