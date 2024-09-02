from sqlalchemy.orm import Session
from models import Level
from schemas import LevelCreate, LevelUpdate

class LevelRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, level_data: LevelCreate):
        db_level = Level(name=level_data.name, order=level_data.order)
        self.db.add(db_level)
        self.db.commit()
        self.db.refresh(db_level)
        return db_level

    def get_by_id(self, level_id: int):
        return self.db.query(Level).filter(Level.id == level_id).first()

    def get_all(self, skip: int = 0, limit: int = 10):
        return self.db.query(Level).offset(skip).limit(limit).all()

    def update(self, level_id: int, level_data: LevelUpdate):
        db_level = self.get_by_id(level_id)
        if db_level:
            db_level.name = level_data.name
            db_level.order = level_data.order
            self.db.commit()
            self.db.refresh(db_level)
        return db_level

    def delete(self, level_id: int):
        db_level = self.get_by_id(level_id)
        if db_level:
            self.db.delete(db_level)
            self.db.commit()
        return db_level
