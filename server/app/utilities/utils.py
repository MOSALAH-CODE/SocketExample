from decimal import Decimal


def decimal_default(obj):
    if isinstance(obj, Decimal):
        # Convert to int if the Decimal is actually a whole number, else float
        return int(obj) if obj % 1 == 0 else float(obj)
    raise TypeError

def convert_decimals(obj):
        """
        Recursively convert all Decimal objects to int or float in a dictionary or list.
        """
        if isinstance(obj, list):
            return [convert_decimals(item) for item in obj]
        elif isinstance(obj, dict):
            return {k: convert_decimals(v) for k, v in obj.items()}
        elif isinstance(obj, Decimal):
            # Convert to int if the Decimal is a whole number, else float
            return int(obj) if obj % 1 == 0 else float(obj)
        else:
            return obj
        
def sort_users_by_honey(users: list, reverse: bool = True) -> list:
    """
    Sorts a list of users by their 'honey' points.
    
    :param users: List of user dictionaries with a 'honey' field.
    :param reverse: If True, sorts in descending order (default). Otherwise, sorts in ascending order.
    :return: A sorted list of users.
    """
    return sorted(users, key=lambda x: x['honey'], reverse=reverse)


def find_user_rank(users: list, user_id: int) -> int:
    """
    Finds the rank of a user in a group based on their 'honey' points.
    
    :param users: List of user dictionaries, sorted by 'honey' in descending order.
    :param user_id: The ID of the user whose rank we want to find.
    :return: The rank of the user (1-based index). If the user is not found, returns -1.
    """
    # Sort users by 'honey' in descending order (if not already sorted)
    sorted_users = sort_users_by_honey(users)
    
    # Find the rank (1-based index)
    for rank, user in enumerate(sorted_users, start=1):
        if user['user_id'] == user_id:
            return rank
    
    # Return -1 if the user is not found
    return -1
