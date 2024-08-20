from pydantic import BaseModel, ConfigDict
from datetime import datetime


class TodoCreate(BaseModel):
    name: str


class TodoResponse(BaseModel):
    id: int
    name: str
    created: datetime

    model_config = ConfigDict(from_attributes=True)


class TodoUpdate(BaseModel):
    name: str
    created: datetime

    model_config = ConfigDict(from_attributes=True)

class ItemConfig(BaseModel):
    triangle_size: int
    triangle_color: str
    circle_size: int
    circle_color: str
    time_visible_ms: int

    model_config = ConfigDict(from_attributes=True)


class ItemConfigResponse(BaseModel):
    id: int
    created: datetime
    triangle_size: int
    triangle_color: str
    circle_size: int
    circle_color: str
    time_visible_ms: int

    model_config = ConfigDict(from_attributes=True)