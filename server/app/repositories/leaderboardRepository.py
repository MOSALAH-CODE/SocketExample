from botocore.exceptions import ClientError
from datetime import datetime
from dynamoDB import get_table
from boto3.dynamodb.conditions import Key
from enums.levelsEnum import Levels
from services.redisService import RedisService
from interfaces.ILeaderboardRepository import ILeaderboardRepository
from utilities.utils import convert_decimals, sort_users_by_honey

class LeaderboardRepository(ILeaderboardRepository):
    def __init__(self, table_name):
        self.table = get_table(table_name)
        self.redis_service = RedisService(self)
        if not self.table:
            raise Exception(f"Failed to initialize LeaderboardRepository. Table {table_name} does not exist or is unavailable.")

    def add_user_to_group(self, user_id: int, honey_points: int):
        level_id = self.get_level_for_user(honey_points)
        group_id = self.redis_service.get_available_group_for_level(level_id)
        
        user_data = {
            'user_id': user_id,
            'group_id': group_id,
            'honey': honey_points,
            'level_id': level_id,
            'updated_at': str(datetime.now())
        }
        
        try:
            self.table.put_item(Item=user_data)
            self.redis_service.save_user(user_data)
            return True
        except ClientError as e:
            return False


    def get_level_for_user(self, honey_points: int):
        if honey_points < 100:
            return Levels.BRONZE.value
        elif honey_points < 200:
            return Levels.SILVER.value
        elif honey_points < 300:
            return Levels.GOLD.value
        else:
            return Levels.PLATINUM.value

    def get_users_in_group(self, level_id: int, group_id: int):
        try:
            response = self.table.query(
                KeyConditionExpression=Key('group_id').eq(group_id) & Key('user_id').gte(0),
                FilterExpression=Key('level_id').eq(level_id)
            )
            return sort_users_by_honey(convert_decimals(response['Items']))
        except ClientError as e:
            return None

    def get_all_users_by_level(self, level_id: int):
        try:
            response = self.table.scan(
                FilterExpression=Key('level_id').eq(level_id)
            )
            return convert_decimals(response['Items'])
        except ClientError as e:
            return None


    def get_user(self, user_id: int):
        try:
            response = self.table.scan(
                FilterExpression=Key('user_id').eq(user_id)
            )
            
            if response['Items']:
                return convert_decimals(response['Items'][0])

        except ClientError as e:
            return None
    
    def add_user_honey_points(self, user_id: int, new_honey_points: int):
        try:
            user = self.redis_service.get_user(user_id)
            
            honey_points = user['honey'] + new_honey_points
            level_id = self.get_level_for_user(honey_points)
            group_id = user['group_id']
            
            if level_id != user['level_id']:
                group_id = self.redis_service.get_available_group_for_level(level_id)
            
            user_data = {
                'user_id': user_id,
                'group_id': group_id,
                'honey': honey_points,
                'level_id': level_id,
                'updated_at': str(datetime.now())
            }
            
            self.table.put_item(Item=user_data)
            self.redis_service.save_user(user_data)
            
            return True
            
        except ClientError as e:
            return False
        
    def remove_user_from_group(self, user_data: dict):
        try:
            self.table.delete_item(Key={'group_id': user_data['group_id'], 'user_id': user_data['user_id']})
            self.redis_service.remove_user(user_data)
            
            return True
        except ClientError as e:
            return False