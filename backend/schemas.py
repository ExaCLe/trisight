from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class ItemConfig(BaseModel):
    triangle_size: int
    triangle_color: str
    circle_size: int
    circle_color: str
    time_visible_ms: int
    orientation: str

    model_config = ConfigDict(from_attributes=True)


class ItemConfigResponse(BaseModel):
    id: int
    created: datetime
    triangle_size: int
    triangle_color: str
    circle_size: int
    circle_color: str
    time_visible_ms: int
    orientation: str

    model_config = ConfigDict(from_attributes=True)


class User(BaseModel):
    name: str
    email: str
    password: str

    model_config = ConfigDict(from_attributes=True)


class ItemConfigResult(BaseModel):
    user_id: Optional[int] = None
    item_config_id: int
    correct: bool
    reaction_time_ms: int
    response: str

    model_config = ConfigDict(from_attributes=True)


class ItemConfigResultResponse(BaseModel):
    id: int
    created: datetime
    user_id: Optional[int] = None
    item_config_id: int
    correct: bool
    reaction_time_ms: int
    response: str

    model_config = ConfigDict(from_attributes=True)
