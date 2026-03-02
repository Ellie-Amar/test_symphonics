from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel


class CamelCaseViewModel(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)


class EventPropertyViewModel(CamelCaseViewModel):
    code: str
    dp_id: int
    time: int
    value: float


class EventBizDataViewModel(CamelCaseViewModel):
    dev_id: str
    data_id: str
    product_id: str
    properties: list[EventPropertyViewModel]


class EventCreateViewModel(CamelCaseViewModel):
    biz_code: Literal["devicePropertyMessage"]
    biz_data: EventBizDataViewModel
    ts: int


class EventResponseViewModel(CamelCaseViewModel):
    status: str
