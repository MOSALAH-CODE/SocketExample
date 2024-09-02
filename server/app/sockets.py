import socketio
from models import Level, Group, Player
from database import get_db
from redis_db import (
    sync_all_groups,
    sync_all_waiting_rooms,
    create_group,
    add_player_to_group,
    remove_player_from_group,
    get_players_in_group,
    is_group_full,
    create_waiting_room,
    add_player_to_waiting_room,
    remove_player_from_waiting_room,
    get_players_in_waiting_room,
    is_waiting_room_empty
)
from redis_db import redisClient

sio_server = socketio.AsyncServer(
    async_mode='asgi',
    cors_allowed_origins=[]
)

sio_app = socketio.ASGIApp(
    socketio_server=sio_server,
    socketio_path='sockets'
)

MAX_PLAYERS_PER_GROUP = 30
MIN_PLAYERS_FOR_GROUP = 20
MIN_SCORE = 40

# Sync data from DB to Redis
# sync_all_groups()
# sync_all_waiting_rooms()

@sio_server.event
async def connect(sid, environ, auth):
    print(f'{sid}: connected')
    await sio_server.emit('join', {'sid': sid})

# @sio_server.event
# async def join_group(sid, data):
#     level_name = data['level']
#     group_name = data['group']
    
#     # Connect to the database
#     db = next(get_db())
    
#     # Fetch the level and group from the database
#     level_obj = db.query(Level).filter(Level.name == level_name).first()
#     group_obj = db.query(Group).filter(Group.name == group_name, Group.level_id == level_obj.id).first()

#     if not level_obj or not group_obj:
#         await sio_server.emit('error', {'message': 'Invalid level or group specified.'}, room=sid)
#         return

#     # Create or get existing waiting room
#     waiting_room_key = create_waiting_room(level_name, group_name)
    
#     # Add player to waiting room
#     add_player_to_waiting_room(level_name, group_name, sid)

#     # Check if the waiting room is ready to move players to the active group
#     if len(get_players_in_waiting_room(level_name, group_name)) >= MIN_PLAYERS_FOR_GROUP:
#         # Create or get existing active group
#         group_key = create_group(level_name, group_name)
        
#         # Move players from waiting room to active group
#         players = get_players_in_waiting_room(level_name, group_name)
#         for player_id in players:
#             # Check if the player has enough score to join the group
#             player = db.query(Player).filter(Player.id == player_id).first()
#             if player and player.score >= MIN_SCORE:
#                 add_player_to_group(level_name, group_name, player_id)
#                 remove_player_from_waiting_room(level_name, group_name, player_id)
#             else:
#                 remove_player_from_waiting_room(level_name, group_name, player_id)
        
#         if is_group_full(level_name, group_name, MAX_PLAYERS_PER_GROUP):
#             # Notify that the group is full and ready
#             await sio_server.emit('room_status', {'status': 'active', 'message': 'Group is full and ready.'}, room=sid)
#         else:
#             await sio_server.emit('room_status', {'status': 'waiting', 'message': 'Waiting for more players.'}, room=sid)
#     else:
#         await sio_server.emit('room_status', {'status': 'waiting', 'message': 'Waiting for more players.'}, room=sid)

# @sio_server.event
# async def is_waiting_room(sid, data):
#     level_name = data['level']
#     group_name = data['group']
    
#     waiting_room_key = f'{level_name}_{group_name}_waiting'
    
#     # Check if the waiting room is ready or still waiting
#     if not is_waiting_room_empty(level_name, group_name):
#         await sio_server.emit('waiting_status', {'status': 'waiting', 'message': 'Waiting for players to be moved to the group.'}, room=sid)
#     else:
#         await sio_server.emit('waiting_status', {'status': 'not_waiting', 'message': 'No players in the waiting room.'}, room=sid)

# @sio_server.event
# async def leave_group(sid, data):
#     level_name = data['level']
#     group_name = data['group']
    
#     # Check and remove player from the active group
#     group_key = f'{level_name}_{group_name}_active'
#     if redisClient.sismember(group_key, sid):
#         remove_player_from_group(level_name, group_name, sid)
#         await sio_server.leave_room(sid, group_key)
#         print(f'{sid} left group {group_key}')
    
#     # Check and remove player from the waiting room
#     waiting_room_key = f'{level_name}_{group_name}_waiting'
#     if redisClient.sismember(waiting_room_key, sid):
#         remove_player_from_waiting_room(level_name, group_name, sid)
#         print(f'{sid} removed from waiting room {waiting_room_key}')

# @sio_server.event
# async def update_score(sid, data):
#     level_name = data["level"]
#     group_name = data["group"]
#     player_id = data["playerId"]
#     change = data["change"]

#     # Connect to the database
#     db = next(get_db())
    
#     # Update the player's score
#     player = db.query(Player).filter(Player.id == player_id).first()
#     if player:
#         player.score += change
#         db.commit()

#     # Fetch the updated leaderboard for the specific group
#     group_key = f'{level_name}_{group_name}_active'
#     players = get_players_in_group(level_name, group_name)

#     leaderboard_data = []
#     for player_id in players:
#         player = db.query(Player).filter(Player.id == player_id).first()
#         if player:
#             leaderboard_data.append({"id": player.id, "name": player.name, "score": player.score})

#     # Broadcast the updated leaderboard to the specific room
#     await sio_server.emit('leaderboard_update', leaderboard_data, room=group_key)

# @sio_server.event
# async def disconnect(sid):
#     print(f'{sid}: disconnected')
#     # Remove the disconnected user from all rooms
#     for level_name in set([key.split('_')[0] for key in redisClient.keys()]):
#         for group_name in set([key.split('_')[1] for key in redisClient.keys()]):
#             group_key = f'{level_name}_{group_name}_active'
#             waiting_room_key = f'{level_name}_{group_name}_waiting'
#             if redisClient.sismember(group_key, sid):
#                 remove_player_from_group(level_name, group_name, sid)
#                 await sio_server.leave_room(sid, group_key)
#                 print(f'{sid} removed from group {group_key}')
#             if redisClient.sismember(waiting_room_key, sid):
#                 remove_player_from_waiting_room(level_name, group_name, sid)
#                 print(f'{sid} removed from waiting room {waiting_room_key}')
