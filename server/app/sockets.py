from services.leaderboardService import LeaderboardService
import socketio

leaderboard_service = LeaderboardService()

sio_server = socketio.AsyncServer(
    async_mode='asgi',
    cors_allowed_origins=[]
)

sio_app = socketio.ASGIApp(
    socketio_server=sio_server,
    socketio_path='sockets'
)

@sio_server.event
async def connect(sid, environ, auth):
    print(f'{sid}: connected')
    await sio_server.emit('join', {'sid': sid})
