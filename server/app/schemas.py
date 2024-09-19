        
from pydantic import BaseModel

class AddUserRequest(BaseModel):
    user_id: int
    honey_points: int

# Request model for updating a user's score
class UpdateUserScoreRequest(BaseModel):
    user_id: int
    new_honey_points: int