from sqlalchemy.orm import Session
from repositories.playerRepository import PlayerRepository
from repositories.groupRepository import GroupRepository
from schemas import PlayerCreate, PlayerUpdate
from exceptions import PlayerNotFoundException, GroupNotFoundException
from fastapi import HTTPException

class PlayerService:
    def __init__(self, db: Session):
        self.player_repository = PlayerRepository(db)
        self.group_repository = GroupRepository(db)

    def create_player(self, player_data: PlayerCreate):
        # Ensure group exists and is not full
        if player_data.group_id is not None:
            if self.group_repository.is_group_full(player_data.group_id, max_players=10):  # Adjust max_players as needed
                raise HTTPException(status_code=400, detail="Group is full")
        return self.player_repository.create(player_data)

    def get_player(self, player_id: int):
        player = self.player_repository.get_by_id(player_id)
        if not player:
            raise PlayerNotFoundException()
        return player

    def get_players(self, skip: int = 0, limit: int = 10):
        return self.player_repository.get_all(skip, limit)

    def update_player(self, player_id: int, player_data: PlayerUpdate):
        player = self.player_repository.update(player_id, player_data.name, player_data.score)
        if not player:
            raise PlayerNotFoundException()
        return player

    def delete_player(self, player_id: int):
        player = self.player_repository.delete(player_id)
        if not player:
            raise PlayerNotFoundException()
        return player

    def add_player_to_group(self, player_id: int, group_id: int):
        # Check if group exists and is not full
        if self.group_repository.is_group_full(group_id, max_players=10):
            raise HTTPException(status_code=400, detail="Group is full")
        player = self.player_repository.add_player_to_group(player_id, group_id)
        if not player:
            raise PlayerNotFoundException()
        return player

    def remove_player_from_group(self, player_id: int):
        player = self.player_repository.remove_player_from_group(player_id)
        if not player:
            raise PlayerNotFoundException()
        return player

    def get_players_in_group(self, group_id: int):
        return self.player_repository.get_players_in_group(group_id)
