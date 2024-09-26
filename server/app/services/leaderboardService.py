from repositories.leaderboardRepository import LeaderboardRepository
from utilities.utils import find_user_rank
from models import User, CreateUser, GetUserLeaderboardRes
from utilities.config_variables import MAX_PLAYERS_PER_GROUP
from enums.levelsEnum import Levels

class LeaderboardService:
    def __init__(self):
        self.repository = LeaderboardRepository("leaderboard")

    def add_user(self, user_id: int, honey_points: int) -> CreateUser:
        """
        Add a user to the leaderboard based on their honey points.
        Automatically assigns the user to a group and level.
        """
        # Determine the user's level based on their honey points
        level_id = self.get_level_for_user(honey_points)

        # Find an appropriate group for the user
        group_id = self.get_or_create_group(level_id)

        # Create user data and insert it into the leaderboard
        user_data = CreateUser(
            user_id=user_id,
            group_id=group_id,
            honey=honey_points,
            level_id=level_id
        )
        
        # Insert the user data into the repository
        self.repository.insert_user(user_data.model_dump()) 

        return user_data


    def get_user_leaderboard(self, user: User) -> GetUserLeaderboardRes:
        """
        Retrieve the leaderboard information for a specific user.
        Adds the user to a group if they aren't assigned to one.
        """
        # Check if the user is already in a group
        if user.group_id == -1:
            # If not, add them to a group and get their data
            user_data = self.add_user(user.user_id, user.honey)
            level_id, group_id = user_data.level_id, user_data.group_id
        else:
            level_id, group_id = user.level_id, user.group_id

        # Fetch all users in the group
        users = self.repository.get_users_in_group(level_id, group_id)

        # Find the rank of the user in the group
        rank = find_user_rank(users, user.user_id)

        # Return the response as a GetUserLeaderboardRes model instance
        return GetUserLeaderboardRes(
            user_id=user.user_id,
            level_id=level_id,
            group_id=group_id,
            honey=user.honey,
            rank=rank,
            users=users
        )

    def get_or_create_group(self, level_id: int) -> int:
        """
        Retrieve an existing group with available space or create a new one.
        """
        # Get the group with the highest ID for the given level
        group_id = self.repository.get_greatest_group_id_for_level(level_id)

        # Check if group is full or doesn't exist (0 indicates no groups found)
        if group_id == 0 or len(self.repository.get_users_in_group(level_id, group_id)) >= MAX_PLAYERS_PER_GROUP:
            group_id += 1  # Increment group_id to create a new group

        return group_id

    def get_level_for_user(self, honey_points: int) -> int:
        """
        Determine the level based on honey points.
        """
        if honey_points < 100:
            return Levels.BRONZE.value
        elif honey_points < 200:
            return Levels.SILVER.value
        elif honey_points < 300:
            return Levels.GOLD.value
        else:
            return Levels.PLATINUM.value