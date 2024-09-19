import boto3
from botocore.exceptions import ClientError
from utilities.config_variables import AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_REGION

# Create a DynamoDB resource
dynamodb = boto3.resource(
    'dynamodb',
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    region_name=AWS_REGION
)

# Function to get a DynamoDB table
def get_table(table_name: str):
    try:
        # Retrieve the table
        table = dynamodb.Table(table_name)
        # Check if the table exists by making a dummy call (optional)
        table.load()  # This will raise an exception if the table doesn't exist
        return table
    except ClientError as e:
        print(f"Unable to connect to table {table_name}: {e.response['Error']['Message']}")
        return None
    except Exception as e:
        print(f"Unexpected error: {e}")
        return None
