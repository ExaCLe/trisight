from pydantic import BaseModel
from datetime import datetime


class TodoCreate(BaseModel):
    name: str


class TodoResponse(BaseModel):
    id: int
    name: str
    created: datetime

    class Config:
        orm_mode = True