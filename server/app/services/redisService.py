import redis
import json
import pickle
from utilities.config_variables import (
    REDIS_CONNECT_TIMEOUT, 
    REDIS_DATABASE, 
    REDIS_HOST, 
    REDIS_PORT,
    REDIS_TTL  # Assuming you have a constant for TTL defined
)

class RedisService:
    def __init__(self):
        self.redisClient = redis.StrictRedis(
            host=REDIS_HOST,
            port=REDIS_PORT,
            db=REDIS_DATABASE,
            socket_timeout=REDIS_CONNECT_TIMEOUT
        )

    def get_user_by_token(self, token: str):
        # Construct cache key
        cache_key = f":1:{token}"
        
        try:
            # Try to get user data from Redis
            user_data = self.redisClient.get(cache_key)
            
            if user_data:
                try:
                    # Try to decode as UTF-8 JSON
                    user_str = user_data.decode("utf-8")
                    user = json.loads(user_str)
                except (UnicodeDecodeError, json.JSONDecodeError):
                    # If decoding or JSON parsing fails, try deserializing with pickle
                    try:
                        user = pickle.loads(user_data)
                    except pickle.UnpicklingError:
                        return None
                
                # Expand the TTL for the cache key
                self.redisClient.expire(cache_key, REDIS_TTL)

                return user
            else:
                # If user_data is None, the key does not exist in Redis
                return None

        except redis.RedisError as e:
            # Log Redis errors
            return None
