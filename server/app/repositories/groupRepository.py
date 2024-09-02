from sqlalchemy.orm import Session
from models import Group, Player
from schemas import GroupCreate

class GroupRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, group_data: GroupCreate, level_id: int):
        db_group = Group(name=group_data.name, level_id=level_id)
        self.db.add(db_group)
        self.db.commit()
        self.db.refresh(db_group)
        return db_group

    def get_by_id(self, group_id: int):
        return self.db.query(Group).filter(Group.id == group_id).first()

    def get_all(self, skip: int = 0, limit: int = 10):
        return self.db.query(Group).offset(skip).limit(limit).all()

    def update(self, group_id: int, name: str):
        db_group = self.get_by_id(group_id)
        if db_group:
            db_group.name = name
            self.db.commit()
            self.db.refresh(db_group)
        return db_group

    def delete(self, group_id: int):
        db_group = self.get_by_id(group_id)
        if db_group:
            self.db.delete(db_group)
            self.db.commit()
        return db_group
    
    def is_group_full(self, group_id: int, max_players: int):
        player_count = self.db.query(Player).filter(Player.group_id == group_id).count()
        return player_count >= max_players
