from app.domain.entities.event import Event


class InMemoryEventRepository:
    def __init__(self) -> None:
        self.events: list[Event] = []

    async def add(self, event: Event) -> None:
        self.events.append(event)
