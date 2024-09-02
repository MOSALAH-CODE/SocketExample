# server/app/repositories/playerRepository.py

from sqlalchemy.orm import Session
from models import Player
from schemas import PlayerCreate, PlayerUpdate

class PlayerRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, player_data: PlayerCreate):
        db_player = Player(name=player_data.name, score=player_data.score, group_id=player_data.group_id)
        self.db.add(db_player)
        self.db.commit()
        self.db.refresh(db_player)
        return db_player

    def get_by_id(self, player_id: int):
        return self.db.query(Player).filter(Player.id == player_id).first()

    def get_all(self, skip: int = 0, limit: int = 10):
        return self.db.query(Player).offset(skip).limit(limit).all()

    def update(self, player_id: int, name: str, score: int):
        db_player = self.get_by_id(player_id)
        if db_player:
            db_player.name = name
            db_player.score = score
            self.db.commit()
            self.db.refresh(db_player)
        return db_player

    def delete(self, player_id: int):
        db_player = self.get_by_id(player_id)
        if db_player:
            self.db.delete(db_player)
            self.db.commit()
        return db_player
    
    def add_players_to_group(self, player_ids: list[int], group_id: int):
        players = self.db.query(Player).filter(Player.id.in_(player_ids)).all()
        
        if not players:
            return None

        for player in players:
            player.group_id = group_id

        self.db.commit()
        for player in players:
            self.db.refresh(player)
        
        return players


    def remove_player_from_group(self, player_id: int):
        player = self.get_by_id(player_id)
        if player:
            player.group_id = None
            self.db.commit()
            self.db.refresh(player)
        return player

    def get_players_in_group(self, group_id: int):
        return self.db.query(Player).filter(Player.group_id == group_id).all()
