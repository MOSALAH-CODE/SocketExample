from botocore.exceptions import ClientError
from dynamoDB import get_table
from boto3.dynamodb.conditions import Key
from utilities.utils import convert_decimals, sort_users_by_honey

class LeaderboardRepository():
    def __init__(self, table_name):
        self.table = get_table(table_name)
        if not self.table:
            raise Exception(f"Failed to initialize LeaderboardRepository. Table {table_name} does not exist or is unavailable.")

    def insert_user(self, user_data: dict):        
        try:
            self.table.put_item(Item=user_data)
            return user_data
        except ClientError as e:
            return False


    def get_users_in_group(self, level_id: int, group_id: int):
        try:
            response = self.table.query(
                KeyConditionExpression=Key('group_id').eq(group_id) & Key('user_id').gte(0),
                FilterExpression=Key('level_id').eq(level_id)
            )
            return sort_users_by_honey(convert_decimals(response['Items']))
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
    
    def update_user_honey_points(self, user: dict, new_honey_points: int, add=False):
        try:
            # Calculate the new honey points
            honey_points = user['honey'] + new_honey_points if add else new_honey_points
            
            # Update the item in the DynamoDB table
            self.table.update_item(
                Key={
                    'group_id': user['group_id'],
                    'user_id': user['user_id']
                },
                UpdateExpression="SET honey = :honey",
                ExpressionAttributeValues={
                    ':honey': honey_points
                }
            )
            
            return honey_points
            
        except Exception as e:
            print(f"Error updating honey points for user {user['user_id']}: {e}")
            return False

        
    def remove_user_from_group(self, user_data: dict):
        try:
            self.table.delete_item(Key={'group_id': user_data['group_id'], 'user_id': user_data['user_id']})
            
            return True
        except ClientError as e:
            return False
    
    def get_greatest_group_id_for_level(self, level_id: int):
        try:
            response = self.table.query(
                IndexName='level_id-index',
                KeyConditionExpression=Key('level_id').eq(level_id),
                ProjectionExpression='group_id',
                ScanIndexForward=False,  # This is used in query, not in scan
                Limit=1  # We only need the highest one
            )
            
            if response['Items']:
                return int(response['Items'][0]['group_id'])  # Return the greatest group_id
            return 0  # No groups found

        except ClientError as e:
            print(f"Error fetching greatest group ID for level {level_id}: {e}")
            return None
