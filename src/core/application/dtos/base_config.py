# -*- coding: utf-8 -*-
from abc import ABC

from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel


class BaseConfig(ABC, BaseModel):
    model_config = ConfigDict(
        extra="ignore",
        frozen=True,
        populate_by_name=True,
        loc_by_alias=True,
        alias_generator=to_camel,
        ser_json_timedelta="iso8601",
        ser_json_bytes="utf8",
    )
