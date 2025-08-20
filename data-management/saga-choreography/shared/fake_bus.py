class FakeEventBus:
    def __init__(self):
        self.published: list[tuple[str, dict]] = []
        self.handlers: dict[str, list] = {}

    async def connect(self): pass
    async def close(self): pass

    async def publish(self, routing_key: str, message: dict):
        self.published.append((routing_key, message))
        # consegna immediata a eventuali subscriber locali (per test end-to-end “in memoria”)
        for h in self.handlers.get(routing_key, []):
            await h(message)

    async def subscribe(self, routing_key: str, handler):
        self.handlers.setdefault(routing_key, []).append(handler)
