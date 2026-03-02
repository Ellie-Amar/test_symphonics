from typing import Protocol
from app.domain.entities.event import Event


class IEventRepository(Protocol):
    async def add(self, event: Event) -> None: ...
