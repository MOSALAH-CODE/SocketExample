from abc import ABC, abstractmethod

class IRedisService(ABC):
    @abstractmethod
    def get_available_group_for_level(self, level_id: int) -> int:
        """ 
        
        """
        pass

    @abstractmethod
    def save_group_to_cache(self, level_id: int, group_id: int):
        """ 
        
        """
        pass

    @abstractmethod
    def save_level_groups(self, level_id: int):
        """ 
        
        """
        pass

    @abstractmethod
    def remove_group_from_cache(self, level_id: int, group_id: int):
        """ 
        
        """
        pass

    @abstractmethod
    def get_users_in_group(self, level_id: int, group_id: int):
        """ 
        
        """
        pass

    @abstractmethod
    def save_user(self, user_data: dict):
        """ 
        
        """
        pass

    @abstractmethod
    def get_user(self, user_id: int):
        """ 
        
        """
        pass
