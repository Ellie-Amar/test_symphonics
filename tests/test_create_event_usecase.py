import asyncio

from app.application.commands.create_event import CreateEventCommand
from app.application.usecases.create_event import CreateEvent
from app.infrastructure.repositories.in_memory.event_repository import (
    InMemoryEventRepository,
)

# Additional use case tests to add later:
#
# - only unsupported codes create no event
# - one supported property creates one event
# - many supported properties create many events
# - time is converted from ms to UTC datetime
# - repo error is handled correctly


def test_create_event_keeps_only_allowed_properties():
    repo = InMemoryEventRepository()
    usecase = CreateEvent(repo)

    command = CreateEventCommand(
        biz_code="devicePropertyMessage",
        dev_id="heater-123",
        data_id="data-123",
        product_id="radiator-v1",
        properties=[
            CreateEventCommand.Property(
                code="instant_power",
                dp_id=1,
                time=1700000000000,
                value=2500,
            ),
            CreateEventCommand.Property(
                code="temp_interior",
                dp_id=2,
                time=1700000000000,
                value=21.5,
            ),
            CreateEventCommand.Property(
                code="mode",
                dp_id=3,
                time=1700000000000,
                value=1,
            ),
        ],
        ts=1700000000000,
    )

    asyncio.run(usecase.execute(command))

    assert [(event.code, event.value) for event in repo.events] == [
        ("instant_power", 2500),
        ("temp_interior", 21.5),
    ]
    for event in repo.events:
        assert event.dev_id == "heater-123"
