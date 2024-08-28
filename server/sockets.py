import socketio

# Setup Socket.IO server
sio_server = socketio.AsyncServer(
    async_mode='asgi',
    cors_allowed_origins=[]
)

sio_app = socketio.ASGIApp(
    socketio_server=sio_server,
    socketio_path='sockets'
)

# Initialize leaderboard data
NUM_LEVELS = 3
GROUPS_PER_LEVEL = 3
PLAYERS_PER_GROUP = 30

def initialize_levels(num_levels, groups_per_level, players_per_group):
    return {
        f"Level {l + 1}": {
            f"Group {g + 1}": [
                {"id": j + 1 + g * players_per_group + l * groups_per_level * players_per_group, "name": f"Player {j + 1}", "score": 0}
                for j in range(players_per_group)
            ]
            for g in range(groups_per_level)
        }
        for l in range(num_levels)
    }

# Initialize the levels with groups and players
levels = initialize_levels(NUM_LEVELS, GROUPS_PER_LEVEL, PLAYERS_PER_GROUP)

# Event: On connection
@sio_server.event
async def connect(sid, environ, auth):
    print(f'{sid}: connected')
    await sio_server.emit('join', {'sid': sid})
    await send_sorted_leaderboard(sid)

# Event: On chat
@sio_server.event
async def chat(sid, message):
    await sio_server.emit('chat', {'sid': sid, 'message': message})

# Event: On disconnect
@sio_server.event
async def disconnect(sid):
    print(f'{sid}: disconnected')

# Event: Update player score
@sio_server.event
async def update_score(sid, data):
    # Data structure: { "level": "Level 1", "group": "Group 1", "playerId": 1, "change": 10 }
    level = data["level"]
    group = data["group"]
    player_id = data["playerId"]
    change = data["change"]
    
    # Update the player's score
    for player in levels[level][group]:
        if player["id"] == player_id:
            player["score"] += change
            break
    
    # Broadcast the updated leaderboard to all clients
    await send_sorted_leaderboard(sid)

# Function to send the sorted leaderboard to all connected clients
async def send_sorted_leaderboard(sid):
    sorted_levels = {
        level_name: {
            group_name: sorted(players, key=lambda p: p["score"], reverse=True)
            for group_name, players in groups.items()
        }
        for level_name, groups in levels.items()
    }
    await sio_server.emit('leaderboard_update', sorted_levels)
