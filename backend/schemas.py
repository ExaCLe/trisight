from datetime import datetime
from typing import List, Optional

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


class UserResponse(BaseModel):
    id: int
    created: datetime
    name: str
    email: str

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


class TestConfig(BaseModel):
    user_id: Optional[int] = None
    name: str
    item_config_ids: List[int]

    model_config = ConfigDict(from_attributes=True)


class TestConfigResponse(BaseModel):
    id: int
    created: datetime
    user_id: Optional[int] = None
    name: str
    item_configs: List[ItemConfigResponse]

    model_config = ConfigDict(from_attributes=True)


class TestConfigResult(BaseModel):
    test_config_id: int
    time: datetime
    correct_answers: int
    wrong_answers: int
    item_config_result_ids: List[int]
    user_id: Optional[int] = None

    model_config = ConfigDict(from_attributes=True)


class TestConfigResultResponse(BaseModel):
    id: int
    created: datetime
    user_id: Optional[int] = None
    test_config_id: int
    time: datetime
    correct_answers: int
    wrong_answers: int
    item_config_results: List[ItemConfigResultResponse]

    model_config = ConfigDict(from_attributes=True)
