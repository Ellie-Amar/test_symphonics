from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Optional
from uuid import UUID


def _utcnow() -> datetime:
    return datetime.now(timezone.utc)


@dataclass(frozen=True)
class Event:
    """
    Dataclass for an event.
    """

    id: UUID
    dev_id: str
    product_id: Optional[str]
    code: str
    value: float
    time: datetime
    synced_to_bq: bool
    created_at: datetime = field(default_factory=_utcnow)
