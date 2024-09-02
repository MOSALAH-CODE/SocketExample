        
from pydantic import BaseModel
from typing import Optional


# Player Models
class PlayerBase(BaseModel):
    name: str
    score: Optional[int] = 0
    group_id: Optional[int] = None

class PlayerCreate(PlayerBase):
    pass

class PlayerUpdate(PlayerBase):
    pass

class PlayerIds(BaseModel):
    ids: list[int]

class Player(PlayerBase):
    id: int
    group_id: Optional[int] = None

    class Config:
        from_attributes = True

# Group Models
class GroupBase(BaseModel):
    name: str

class GroupCreate(GroupBase):
    pass

class GroupUpdate(GroupBase):
    pass

class Group(GroupBase):
    id: int
    level_id: int

    class Config:
        from_attributes = True

# Level Models
class LevelBase(BaseModel):
    name: str
    order: int

class LevelCreate(LevelBase):
    pass

class LevelUpdate(LevelBase):
    pass

class Level(LevelBase):
    id: int

    class Config:
        from_attributes = True

