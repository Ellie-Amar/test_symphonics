from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class CreateEventCommand:
    @dataclass(frozen=True)
    class Property:
        code: str
        dp_id: int
        time: int
        value: float

    biz_code: str
    dev_id: str
    data_id: str
    product_id: str
    properties: list[Property]
    ts: int

    @staticmethod
    def from_payload(payload: Any) -> "CreateEventCommand":
        return CreateEventCommand(
            biz_code=payload.biz_code,
            dev_id=payload.biz_data.dev_id,
            data_id=payload.biz_data.data_id,
            product_id=payload.biz_data.product_id,
            properties=[
                CreateEventCommand.Property(
                    code=property_item.code,
                    dp_id=property_item.dp_id,
                    time=property_item.time,
                    value=property_item.value,
                )
                for property_item in payload.biz_data.properties
            ],
            ts=payload.ts,
        )
