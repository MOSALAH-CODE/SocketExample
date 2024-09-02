# server/app/routers/players.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from services.playerService import PlayerService
from schemas import Player, PlayerCreate, PlayerUpdate
from exceptions import PlayerNotFoundException

router = APIRouter(
    prefix='/api/v1/players',
    tags=['Players'],
)

def get_player_service(db: Session = Depends(get_db)):
    return PlayerService(db)

@router.post('/', response_model=Player)
def create_new_player(player: PlayerCreate, service: PlayerService = Depends(get_player_service)):
    return service.create_player(player)

@router.get('/', response_model=list[Player])
def read_players(skip: int = 0, limit: int = 10, service: PlayerService = Depends(get_player_service)):
    return service.get_players(skip=skip, limit=limit)

@router.put('/{player_id}/', response_model=Player)
def update_existing_player(player_id: int, player: PlayerUpdate, service: PlayerService = Depends(get_player_service)):
    try:
        return service.update_player(player_id, player)
    except PlayerNotFoundException:
        raise HTTPException(status_code=404, detail="Player not found")

@router.delete('/{player_id}/', response_model=Player)
def delete_existing_player(player_id: int, service: PlayerService = Depends(get_player_service)):
    try:
        return service.delete_player(player_id)
    except PlayerNotFoundException:
        raise HTTPException(status_code=404, detail="Player not found")

@router.post('/{player_id}/add_to_group/{group_id}/', response_model=Player)
def add_player_to_group(player_id: int, group_id: int, service: PlayerService = Depends(get_player_service)):
    try:
        return service.add_player_to_group(player_id, group_id)
    except PlayerNotFoundException:
        raise HTTPException(status_code=404, detail="Player not found")
    except HTTPException as e:
        raise e

@router.post('/{player_id}/remove_from_group/', response_model=Player)
def remove_player_from_group(player_id: int, service: PlayerService = Depends(get_player_service)):
    try:
        return service.remove_player_from_group(player_id)
    except PlayerNotFoundException:
        raise HTTPException(status_code=404, detail="Player not found")

@router.get('/group/{group_id}/', response_model=list[Player])
def get_players_in_group(group_id: int, service: PlayerService = Depends(get_player_service)):
    return service.get_players_in_group(group_id)
