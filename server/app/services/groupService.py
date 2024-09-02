from sqlalchemy.orm import Session
from repositories.groupRepository import GroupRepository
from schemas import GroupCreate, GroupUpdate
from exceptions import GroupNotFoundException

class GroupService:
    def __init__(self, db: Session):
        self.repository = GroupRepository(db)

    def create_group(self, group_data: GroupCreate, level_id: int):
        return self.repository.create(group_data, level_id)

    def get_group(self, group_id: int):
        group = self.repository.get_by_id(group_id)
        if not group:
            raise GroupNotFoundException()
        return group

    def get_groups(self, skip: int = 0, limit: int = 10):
        return self.repository.get_all(skip, limit)

    def update_group(self, group_id: int, group_data: GroupUpdate):
        group = self.repository.update(group_id, group_data.name)
        if not group:
            raise GroupNotFoundException()
        return group

    def delete_group(self, group_id: int):
        group = self.repository.delete(group_id)
        if not group:
            raise GroupNotFoundException()
        return group
