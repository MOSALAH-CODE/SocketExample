from pydantic import BaseModel, Field
from typing import Any, List
from datetime import datetime


class StandardResponse(BaseModel):
    success: bool
    error: Any = None
    body: Any

class User(BaseModel):
    user_id: int
    honey: int
    level_id: int
    group_id: int
    
    class Config:
        orm_mode = True  # Allows compatibility with ORMs and dictionary-based data

class CreateUser(User):
    updated_at: str = Field(default_factory=lambda: datetime.now().isoformat())

    class Config:
        orm_mode = True  # Allows compatibility with ORMs and dictionary-based data

class DisplayOtherUser(BaseModel):
    user_id: int
    honey: int

    class Config:
        orm_mode = True  # Allows compatibility with ORMs and dictionary-based data


class GetUserLeaderboardRes(User):
    rank: int
    users: List[DisplayOtherUser]
    
    class Config:
        orm_mode = True  # Allows compatibility with ORMs and dictionary-based data

