        
from pydantic import BaseModel


# Request model for updating a user's score
class UpdateUserScoreRequest(BaseModel):
    new_honey_points: int