from fastapi import APIRouter, HTTPException
from schemas import AddUserRequest, UpdateUserScoreRequest
from services.leaderboardService import LeaderboardService


router = APIRouter(
    prefix='/api/v1/leaderboard',
    tags=['Users'],
)

leaderboard_service = LeaderboardService()


@router.get("/user/{user_id}/")
async def get_user_info(user_id: int):
    user = leaderboard_service.get_user_info(user_id)
    if user is not None:
        return user
    else:
        raise HTTPException(status_code=404, detail="User not found")

@router.post("/user/")
async def add_user(request: AddUserRequest):
    added = leaderboard_service.add_user(request.user_id, request.honey_points)
    return {"added": added}

@router.put("/user/add_honey_points")
async def add_honey_points(request: UpdateUserScoreRequest):
    added = leaderboard_service.add_user_honey_points(request.user_id, request.new_honey_points)
    return {"added": added}

@router.delete("/user/{user_id}/")
async def remove_user_from_group(user_id: int):
    removed = leaderboard_service.remove_user(user_id)
    return {"removed": removed}

@router.get("/level/{level_id}/group/{group_id}/users/")
async def get_users_in_group(level_id: int, group_id: int):
    users = leaderboard_service.get_users_in_group(level_id, group_id)
    if users:
        return users
    else:
        raise HTTPException(status_code=404, detail="No users found in this group")

