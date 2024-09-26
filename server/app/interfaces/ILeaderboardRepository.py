from abc import ABC, abstractmethod

class ILeaderboardRepository(ABC):
    @abstractmethod
    def add_user_to_group(self, group_id: int, level_id: int):
        """ Add a user to the leaderboard """
        pass

    @abstractmethod
    def get_level_for_user(self, level_id: int):
        """ Get level for the user based on honey points """
        pass
    
    @abstractmethod
    def get_users_in_group(self, level_id: int, group_id: int):
        """ Retrieve all users in a specific group """
        pass

    @abstractmethod
    def update_user_honey_points(self, level_id: int):
        """ Update the user's score and possibly move them to another group """
        pass

    @abstractmethod
    def remove_user_from_group(self, level_id: int):
        """ Remove user from a group (if they are moving to another group) """
        pass

    @abstractmethod
    def get_all_users_by_level(self, level_id: int):
        """ """
        pass

    @abstractmethod
    def get_user(self, user_id: int):
        """ """
        pass