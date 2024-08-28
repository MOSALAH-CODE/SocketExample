import redis
from utilities.config_variables import REDIS_CONNECT_TIMEOUT, REDIS_DATABASE, REDIS_HOST, REDIS_PORT, REDIS_TTL
from models import Level, Group, Player
from database import get_db

redisClient = redis.StrictRedis(
    host=REDIS_HOST,
    port=REDIS_PORT,
    db=REDIS_DATABASE,
    socket_timeout=REDIS_CONNECT_TIMEOUT
)

def sync_groups(level_name, group_name, players):
    group_key = f'{level_name}_{group_name}_active'
    redisClient.delete(group_key)
    for player_id in players:
        redisClient.sadd(group_key, player_id)

def sync_waiting_rooms(level_name, group_name, players):
    waiting_room_key = f'{level_name}_{group_name}_waiting'
    redisClient.delete(waiting_room_key)
    for player_id in players:
        redisClient.sadd(waiting_room_key, player_id)

def sync_all_groups():
    db = next(get_db())
    levels = db.query(Level).all()
    for level in levels:
        groups = db.query(Group).filter(Group.level_id == level.id).all()
        for group in groups:
            players = db.query(Player).filter(Player.group_id == group.id).all()
            player_ids = [player.id for player in players]
            sync_groups(level.name, group.name, player_ids)

def sync_all_waiting_rooms():
    db = next(get_db())
    levels = db.query(Level).all()
    for level in levels:
        groups = db.query(Group).filter(Group.level_id == level.id).all()
        for group in groups:
            players = db.query(Player).filter(Player.group_id == group.id).all()
            player_ids = [player.id for player in players]
            sync_waiting_rooms(level.name, group.name, player_ids)


def create_group(level_name, group_name):
    """Create a new group in Redis."""
    group_key = f'{level_name}_{group_name}_active'
    redisClient.delete(group_key)  # Ensure no stale data
    return group_key

def add_player_to_group(level_name, group_name, player_id):
    """Add a player to a group in Redis."""
    group_key = f'{level_name}_{group_name}_active'
    redisClient.sadd(group_key, player_id)

def remove_player_from_group(level_name, group_name, player_id):
    """Remove a player from a group in Redis."""
    group_key = f'{level_name}_{group_name}_active'
    redisClient.srem(group_key, player_id)

def get_players_in_group(level_name, group_name):
    """Get all players in a group from Redis."""
    group_key = f'{level_name}_{group_name}_active'
    return redisClient.smembers(group_key)

def is_group_full(level_name, group_name, max_players):
    """Check if a group has reached the maximum number of players."""
    group_key = f'{level_name}_{group_name}_active'
    current_size = redisClient.scard(group_key)
    return current_size >= max_players

def create_waiting_room(level_name, group_name):
    """Create a waiting room for players."""
    waiting_room_key = f'{level_name}_{group_name}_waiting'
    redisClient.delete(waiting_room_key)  # Ensure no stale data
    return waiting_room_key

def add_player_to_waiting_room(level_name, group_name, player_id):
    """Add a player to the waiting room."""
    waiting_room_key = f'{level_name}_{group_name}_waiting'
    redisClient.sadd(waiting_room_key, player_id)

def remove_player_from_waiting_room(level_name, group_name, player_id):
    """Remove a player from the waiting room."""
    waiting_room_key = f'{level_name}_{group_name}_waiting'
    redisClient.srem(waiting_room_key, player_id)

def get_players_in_waiting_room(level_name, group_name):
    """Get all players in the waiting room from Redis."""
    waiting_room_key = f'{level_name}_{group_name}_waiting'
    return redisClient.smembers(waiting_room_key)

def is_waiting_room_empty(level_name, group_name):
    """Check if the waiting room is empty."""
    waiting_room_key = f'{level_name}_{group_name}_waiting'
    return redisClient.scard(waiting_room_key) == 0
