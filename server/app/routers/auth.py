from http.client import HTTPException
import jwt
from fastapi import Depends, HTTPException, status, Header
from sqlalchemy import text
from sqlalchemy.orm import Session
from redis_db import get_user_from_redis, save_user_to_redis
from database import get_db
from models import User
from utilities.config_variables import SECRET_KEY, ALGORITHM


async def find_token_in_DB(db, token):

    query = text(
        """SELECT tokens.id AS tokenId, 
                tokens.user_id AS userId,
                IFNULL(user_meta.`value`->>'$.honeyPoints', 0) as honey
            FROM user_tokens AS tokens
                JOIN users ON users.id = tokens.user_id 
                LEFT JOIN user_meta ON user_meta.user_id = tokens.user_id AND user_meta.`key` = 5  
            WHERE access_token = :token
                AND tokens.is_deleted = 0
                AND users.is_deleted = 0;""")
    user = db.execute(query, {"token": token}).first()
    if user:
        user = User.from_query_result(user)
        return user
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED)


async def check_correct_token_request(authorization):
    if authorization:
        if authorization.startswith("Token"):
            try:
                return authorization[len("Token"):].strip()
            except:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED)

    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED)


async def get_current_user(authorization: str = Header(None), db: Session = Depends(get_db)):
    tokenValue = await check_correct_token_request(authorization)
    if tokenValue:
        jwt.decode(tokenValue, SECRET_KEY, algorithms=[ALGORITHM])
        userFromRedis = await get_user_from_redis(tokenValue)
        if (userFromRedis):
            return userFromRedis
        else:
            userFromDb = await find_token_in_DB(db, tokenValue)
            await save_user_to_redis(tokenValue, userFromDb)
            return userFromDb
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED)
