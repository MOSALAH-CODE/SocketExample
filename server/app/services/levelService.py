from sqlalchemy.orm import Session
from repositories.levelRepository import LevelRepository
from schemas import LevelCreate, LevelUpdate
from exceptions import LevelNotFoundException

class LevelService:
    def __init__(self, db: Session):
        self.repository = LevelRepository(db)

    def create_level(self, level_data: LevelCreate):
        return self.repository.create(level_data)

    def get_level(self, level_id: int):
        level = self.repository.get_by_id(level_id)
        if not level:
            raise LevelNotFoundException()
        return level

    def get_levels(self, skip: int = 0, limit: int = 10):
        return self.repository.get_all(skip, limit)

    def update_level(self, level_id: int, level_data: LevelUpdate):
        level = self.repository.update(level_id, level_data)
        if not level:
            raise LevelNotFoundException()
        return level

    def delete_level(self, level_id: int):
        level = self.repository.delete(level_id)
        if not level:
            raise LevelNotFoundException()
        return level
