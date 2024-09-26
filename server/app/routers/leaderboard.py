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
    info = leaderboard_service.get_user_leaderboard(user.user_id)
    
    if info is None:
        info = leaderboard_service.add_user(user.user_id, user.honey)
    elif info['honey'] != user.honey:
        leaderboard_service.update_user_honey_points(user.user_id, user.honey)
        info['honey'] = user.honey
    
    users = leaderboard_service.get_users_in_group(info['level_id'], info['group_id'])
    
    info['users'] = users
    
    return info
