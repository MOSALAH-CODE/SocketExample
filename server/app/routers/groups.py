from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from services.groupService import GroupService
from schemas import Group, GroupCreate, GroupUpdate
from exceptions import GroupNotFoundException

router = APIRouter(
    prefix='/api/v1/groups',
    tags=['Groups'],
)

def get_group_service(db: Session = Depends(get_db)):
    return GroupService(db)

@router.post('/', response_model=Group)
def create_new_group(group: GroupCreate, level_id: int, service: GroupService = Depends(get_group_service)):
    return service.create_group(group, level_id)

@router.get('/', response_model=list[Group])
def read_groups(skip: int = 0, limit: int = 10, service: GroupService = Depends(get_group_service)):
    return service.get_groups(skip=skip, limit=limit)

@router.get('/{group_id}', response_model=Group)
def read_group(group_id: int, service: GroupService = Depends(get_group_service)):
    try:
        return service.get_group(group_id)
    except GroupNotFoundException:
        raise HTTPException(status_code=404, detail="Group not found")

@router.put('/{group_id}', response_model=Group)
def update_group(group_id: int, group: GroupUpdate, service: GroupService = Depends(get_group_service)):
    try:
        return service.update_group(group_id, group)
    except GroupNotFoundException:
        raise HTTPException(status_code=404, detail="Group not found")

@router.delete('/{group_id}')
def delete_group(group_id: int, service: GroupService = Depends(get_group_service)):
    try:
        service.delete_group(group_id)
        return {"detail": "Group deleted successfully"}
    except GroupNotFoundException:
        raise HTTPException(status_code=404, detail="Group not found")
