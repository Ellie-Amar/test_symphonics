from __future__ import annotations

from datetime import datetime, timezone
from uuid import uuid4

from app.application.commands.create_event import CreateEventCommand
from app.application.ports.event_repository import IEventRepository
from app.domain.entities.event import Event

ALLOWED_EVENT_CODES = {"instant_power", "temp_interior"}


class CreateEvent:
    def __init__(self, repo: IEventRepository) -> None:
        self.repo = repo

    async def execute(self, command: CreateEventCommand) -> None:
        for property_item in command.properties:
            if property_item.code not in ALLOWED_EVENT_CODES:
                continue

            event = Event(
                id=uuid4(),
                dev_id=command.dev_id,
                product_id=command.product_id,
                code=property_item.code,
                value=property_item.value,
                time=_from_unix_timestamp_ms(property_item.time),
                synced_to_bq=False,
            )
            # TODO batch insert for better performances
            await self.repo.add(event)


def _from_unix_timestamp_ms(value: int) -> datetime:
    return datetime.fromtimestamp(value / 1000, tz=timezone.utc)
