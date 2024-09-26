import redis
from utilities.config_variables import REDIS_CONNECT_TIMEOUT, REDIS_DATABASE, REDIS_HOST, REDIS_PORT, REDIS_TTL, MAX_PLAYERS_PER_GROUP
import json
from interfaces.ILeaderboardRepository import ILeaderboardRepository
from interfaces.IRedisService import IRedisService
from utilities.utils import sort_users_by_honey

class RedisService(IRedisService):
    def __init__(self, leaderboard_repository: ILeaderboardRepository):
        self.redisClient = redis.StrictRedis(
            host=REDIS_HOST,
            port=REDIS_PORT,
            db=REDIS_DATABASE,
            socket_timeout=REDIS_CONNECT_TIMEOUT
        )
        
        self.leaderboard_repository = leaderboard_repository
    
    def get_available_group_for_level(self, level_id: int) -> int:
        # Fetch the list of group IDs for the level from Redis
        group_key = f"level:{level_id}:groups"
        groups_json = self.redisClient.get(group_key)
        
        # If not in Redis, fetch from DynamoDB and cache it
        if not groups_json:
            # Fetch all groups for the level from DynamoDB
            group_ids = self.save_level_groups(level_id)
        else:
            # Load groups from Redis
            group_ids = json.loads(groups_json)
        
        # Check for an available group with less than 30 users
        for group_id in group_ids:
            if len(self.get_users_in_group(level_id, group_id)) < MAX_PLAYERS_PER_GROUP:
                return group_id
        
        # If no available group, create a new one by incrementing on the last group id
        # Assuming group_id is an integer and auto-increment logic is acceptable
        new_group_id = max(map(int, group_ids)) + 1 if group_ids else 1
        self.save_group_to_cache(level_id, new_group_id)
        
        return new_group_id

    def save_group_to_cache(self, level_id: int, group_id: int):
        group_key = f"level:{level_id}:groups"
        groups_json = self.redisClient.get(group_key)
        
        if groups_json:
            groups = json.loads(groups_json)
        else:
            groups = []
        
        if group_id not in groups:
            groups.append(group_id)
            self.redisClient.set(group_key, json.dumps(groups), ex=REDIS_TTL)

    def save_level_groups(self, level_id: int):
        # Fetch all groups for the level from DynamoDB and cache them
        users = self.leaderboard_repository.get_all_users_by_level(level_id)
        group_ids = []
        groups_users = {}
        if users:
            for user in users:
                group_id = int(user['group_id'])
                user_id = int(user['user_id'])
                
                if group_id not in group_ids:
                    group_ids.append(group_id)
                    groups_users.setdefault(group_id, [])
                
                groups_users[group_id].append(user_id)

                self.redisClient.set(f"user:{user_id}", json.dumps(user), ex=REDIS_TTL)

            for group_id in group_ids:
                self.redisClient.set(f"level:{level_id}:group:{group_ids}:users", json.dumps(groups_users[group_id]), ex=REDIS_TTL)
            
            self.redisClient.set(f"level:{level_id}:groups", json.dumps(group_ids), ex=REDIS_TTL)

        return group_ids
    
    def remove_group_from_cache(self, level_id: int, group_id: int):
        group_key = f"level:{level_id}:groups"
        groups_json = self.redisClient.get(group_key)
        
        if groups_json:
            groups = json.loads(groups_json)
            if group_id in groups:
                groups.remove(group_id)
                self.redisClient.set(group_key, json.dumps(groups), ex=REDIS_TTL)
    
    def get_users_in_group(self, level_id: int, group_id: int):
        # Try to get users from Redis
        cache_key = f"level:{level_id}:group:{group_id}:users"
        users_json = self.redisClient.get(cache_key)
        
        if users_json:
            users = json.loads(users_json)
            return users
        
        # If not in cache, fetch from DynamoDB and cache the result
        users = self.leaderboard_repository.get_users_in_group(level_id, group_id)
        
        if users:
            self.redisClient.set(cache_key, json.dumps(users), ex=REDIS_TTL)
            return users
        
        return []
    
    def save_user(self, user_data: dict):
        # Try to get users from Redis
        cache_key = f"level:{user_data['level_id']}:group:{user_data['group_id']}:users"
        users_json = self.redisClient.get(cache_key)

        
        if users_json:
            users = json.loads(users_json)
        else:
            users = []

        users = [user for user in users if user['user_id'] != user_data['user_id']]
        users.append(user_data)

        self.redisClient.set(f"user:{user_data['user_id']}", json.dumps(user_data), ex=REDIS_TTL)

        if users:
            self.redisClient.set(cache_key, json.dumps(sort_users_by_honey(users)), ex=REDIS_TTL)
            return users
        
        return []
    
    def remove_user(self, user_data: dict):
        # Try to get users from Redis
        cache_key = f"level:{user_data['level_id']}:group:{user_data['group_id']}:users"
        users_json = self.redisClient.get(cache_key)
        
        if users_json:
            users = json.loads(users_json)
        else:
            users = []      
        
        # Check if the user exists in the list of users and remove them
        users = [user for user in users if user['user_id'] != user_data['user_id']]
        
        self.redisClient.set(cache_key, json.dumps(sort_users_by_honey(users)), ex=REDIS_TTL)
        
        # Remove the specific user's cache
        user_cache_key = f"user:{user_data['user_id']}"
        self.redisClient.delete(user_cache_key)
        
    def get_user(self, user_id: int):
        # Try to get users from Redis
        cache_key = f"user:{user_id}"
        user_json = self.redisClient.get(cache_key)
        
        if user_json:
            user = json.loads(user_json)
            return user
        
        # If not in cache, fetch from DynamoDB and cache the result
        user = self.leaderboard_repository.get_user(user_id)

        if user:
            # Cache the user IDs for future use
            self.redisClient.set(cache_key, json.dumps(user), ex=REDIS_TTL)
            return user
        
        return None
    
    def get_all_level_group_ids(self, level_id):
        # Try to get groups from Redis
        cache_key = f"level:{level_id}:groups"
        groups_json = self.redisClient.get(cache_key)
        
        if groups_json:
            groups = json.loads(groups_json)
            return groups
        
        # If not in cache, fetch from DynamoDB and cache the result
        # groups = self.leaderboard_repository.get_all_level_groups(level_id)