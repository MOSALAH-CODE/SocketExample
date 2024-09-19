from repositories.leaderboardRepository import LeaderboardRepository
from services.redisService import RedisService
from utilities.utils import find_user_rank

class LeaderboardService:
    def __init__(self):
        self.repository = LeaderboardRepository("leaderboard")
        self.redis_service = RedisService(self.repository)

    def add_user(self, user_id: int, honey_points: int):
        user = self.redis_service.get_user(user_id)
        
        if user:
            return False
        
        return self.repository.add_user_to_group(user_id, honey_points)
    
    def get_user_info(self, user_id: int):
        user = self.redis_service.get_user(user_id)
        
        if not user:
            return None
        
        group_users = self.redis_service.get_users_in_group(user['level_id'], user['group_id'])
        user['rank'] = -1
        
        if group_users:
            user['rank'] = find_user_rank(group_users, user_id)
        
        return user
    
    def add_user_honey_points(self, user_id: int, new_honey_points: int):
        user = self.redis_service.get_user(user_id)
        
        if not user:
            return False
        
        return self.repository.add_user_honey_points(user_id, new_honey_points)

    def remove_user(self, user_id: int):
        user = self.redis_service.get_user(user_id)
        
        if not user:
            return False
        
        return self.repository.remove_user_from_group(user)


    def get_users_in_group(self, level_id: int, group_id: int):
        users = self.redis_service.get_users_in_group(level_id, group_id)
        return users