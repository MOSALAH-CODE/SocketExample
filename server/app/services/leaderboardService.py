from repositories.leaderboardRepository import LeaderboardRepository
from utilities.utils import find_user_rank
from datetime import datetime
from models import User
from utilities.config_variables import MAX_PLAYERS_PER_GROUP
from enums.levelsEnum import Levels

class LeaderboardService:
    def __init__(self):
        self.repository = LeaderboardRepository("leaderboard")

    def add_user(self, user_id: int, honey_points: int):
        level_id = self.get_level_for_user(honey_points)
        group_id = self.repository.get_greatest_group_id_for_level(level_id)
        
        users = self.repository.get_users_in_group(level_id, group_id)
        if (users and len(users) >= MAX_PLAYERS_PER_GROUP) or group_id == 0:
            group_id = group_id + 1
        
        user_data = {
            'user_id': user_id,
            'group_id': group_id,
            'honey': honey_points,
            'level_id': level_id,
            'updated_at': str(datetime.now())
        }
        return self.repository.insert_user(user_data)

    def get_user_leaderboard(self, user: User):
        info = {
            'user_id': user.user_id,
            'level_id': user.level_id,
            'group_id': user.group_id,
            'honey': user.honey,
            'users': [],
            'rank': 0
        }
        
        if user.group_id == -1:
            info = self.add_user(user.user_id, user.honey)

        users = self.repository.get_users_in_group(info['level_id'], info['group_id'])
        
        info['users'] = users
        info['rank'] = find_user_rank(users, user.user_id)
        
        return info

    def get_level_for_user(self, honey_points: int):
        if honey_points < 100:
            return Levels.BRONZE.value
        elif honey_points < 200:
            return Levels.SILVER.value
        elif honey_points < 300:
            return Levels.GOLD.value
        else:
            return Levels.PLATINUM.value