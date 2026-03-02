from sqlalchemy.ext.asyncio import AsyncSession

from app.application.ports.event_repository import IEventRepository
from app.domain.entities.event import Event
from app.infrastructure.db.models.event import EventORM


class EventRepositorySQL(IEventRepository):
    """Async SQLAlchemy repository for events (PostgreSQL)."""

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def add(self, event: Event) -> None:
        event_orm = EventORM(
            id=event.id,
            dev_id=event.dev_id,
            product_id=event.product_id,
            code=event.code,
            value=event.value,
            time=event.time,
            synced_to_bq=event.synced_to_bq,
            created_at=event.created_at,
        )
        self.session.add(event_orm)
        await self.session.commit()
