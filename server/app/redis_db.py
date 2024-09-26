import redis
import json
from utilities.error_handling import handle_exception_standard_messages

from models import User
from utilities.config_variables import REDIS_CONNECT_TIMEOUT, REDIS_DATABASE, REDIS_HOST, REDIS_PORT, REDIS_TTL

redisClient = redis.StrictRedis(
    host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DATABASE, socket_timeout=REDIS_CONNECT_TIMEOUT)


async def get_user_from_redis(token: str):
    try:
        if redisClient.exists(token):
            userData = json.loads(redisClient.get(token).decode("utf-8"))
            user = User(
                token_id=userData["tokenId"],
                user_id=userData["userId"],
                courseId=userData["courseId"],
                language=userData["language"],
                batchData=userData["batchData"])

            return user
        else:
            return None
    except:
        return None


async def save_user_to_redis(token: str,
                             user: User):
    try:
        if redisClient.exists(token) == False:
            redisClient.set(token, json.dumps(user.model_dump()), REDIS_TTL)
    except Exception as e:
        handle_exception_standard_messages(e)
