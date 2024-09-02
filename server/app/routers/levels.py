from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from services.levelService import LevelService
from schemas import LevelCreate, LevelUpdate
from exceptions import LevelNotFoundException

router = APIRouter(
    prefix='/api/v1/levels',
    tags=['Levels'],
)

def get_level_service(db: Session = Depends(get_db)):
    return LevelService(db)

@router.post('/create_level', response_model=LevelCreate)
def create_new_level(level: LevelCreate, service: LevelService = Depends(get_level_service)):
    return service.create_level(level)

@router.get('/get_levels')
def get_levels(skip: int = 0, limit: int = 10, service: LevelService = Depends(get_level_service)):
    return service.get_levels(skip=skip, limit=limit)

@router.get('/{level_id}')
def get_level(level_id: int, service: LevelService = Depends(get_level_service)):
    try:
        return service.get_level(level_id)
    except LevelNotFoundException:
        raise HTTPException(status_code=404, detail="Level not found")

@router.put('/{level_id}')
def update_existing_level(level_id: int, level: LevelUpdate, service: LevelService = Depends(get_level_service)):
    try:
        return service.update_level(level_id, level)
    except LevelNotFoundException:
        raise HTTPException(status_code=404, detail="Level not found")

@router.delete('/{level_id}')
def delete_existing_level(level_id: int, service: LevelService = Depends(get_level_service)):
    try:
        service.delete_level(level_id)
        return {"detail": "Level deleted successfully"}
    except LevelNotFoundException:
        raise HTTPException(status_code=404, detail="Level not found")
