from http.client import HTTPException
import jwt
from typing import Optional
from fastapi import HTTPException, status, Header
from utilities.config_variables import SECRET_KEY, ALGORITHM
from services.redisService import RedisService
from models import User
from repositories.leaderboardRepository import LeaderboardRepository

leaderboard_repository = LeaderboardRepository("leaderboard")
redis_service = RedisService()

async def check_correct_token_request(authorization: str) -> Optional[str]:
    if authorization and authorization.startswith("Token "):
        return authorization[len("Token "):].strip()
    # Raise an HTTPException if the token format is incorrect or missing
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED
    )


async def get_current_user(authorization: Optional[str] = Header(None)):
    # Create a generic 401 Unauthorized exception
    unauthorized_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED
    )

    # Check and decode the token
    token_value = await check_correct_token_request(authorization)
    
    try:
        jwt.decode(token_value, SECRET_KEY, algorithms=[ALGORITHM])
    except jwt.PyJWTError:
        raise unauthorized_exception

    # Retrieve the user from Redis
    user_from_redis = redis_service.get_user_by_token(token_value)
    if not user_from_redis:
        raise unauthorized_exception

    user_from_dynamo = leaderboard_repository.get_user(user_from_redis['id'])
    
    honey = 0
    if 'honey' in user_from_redis:
        honey = user_from_redis.get('honey')
        if 'honey' in user_from_dynamo and user_from_dynamo.get('honey') != honey:
            leaderboard_repository.update_user_honey_points(user_from_dynamo, honey)
    
    # Return the authenticated user
    return User(
        user_id=user_from_redis.get('id'),
        honey=honey,
        level_id=user_from_dynamo.get('level_id') if user_from_dynamo else -1,
        group_id=user_from_dynamo.get('group_id') if user_from_dynamo else -1,
    )