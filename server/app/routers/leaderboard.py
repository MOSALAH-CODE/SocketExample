from fastapi import APIRouter, Depends
from services.leaderboardService import LeaderboardService
from routers.auth import get_current_user
from models import User


router = APIRouter(
    prefix='/api/v1/leaderboard',
    tags=['Users'],
)

leaderboard_service = LeaderboardService()


@router.get("/user")
async def get_user_leaderboard(user: User = Depends(get_current_user)):
    info = leaderboard_service.get_user_leaderboard(user)
    return info
