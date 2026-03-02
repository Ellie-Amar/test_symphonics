from __future__ import annotations

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.application.commands.create_event import CreateEventCommand
from app.application.ports.event_repository import IEventRepository
from app.application.usecases.create_event import CreateEvent
from app.infrastructure.db.dependencies import get_db
from app.infrastructure.repositories.sql.event_repository import EventRepositorySQL
from app.interface.view_models.event_view_models import (
    EventCreateViewModel,
    EventResponseViewModel,
)

router = APIRouter(prefix="/message", tags=["events"])


def get_event_repo(
    session: AsyncSession = Depends(get_db),
) -> IEventRepository:
    return EventRepositorySQL(session)


def get_create_event_uc(
    repo: IEventRepository = Depends(get_event_repo),
) -> CreateEvent:
    return CreateEvent(repo)


@router.post(
    "",
    response_model=EventResponseViewModel,
    status_code=status.HTTP_202_ACCEPTED,
)
async def create_event(
    payload: EventCreateViewModel,
    usecase: CreateEvent = Depends(get_create_event_uc),
) -> EventResponseViewModel:
    await usecase.execute(CreateEventCommand.from_payload(payload))
    return EventResponseViewModel(status="accepted")
