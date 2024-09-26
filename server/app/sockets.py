from repositories.leaderboardRepository import LeaderboardRepository
from services.redisService import RedisService
import socketio

repository = LeaderboardRepository("leaderboard")
redis_service = RedisService(repository)

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
