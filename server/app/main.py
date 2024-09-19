from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import engine
from sockets import sio_app
from utilities.config_variables import FASTAPI_HOST, FASTAPI_PORT_NUMBER
from routers import leaderboard

app = FastAPI()

app.include_router(leaderboard.router)


app.mount('/', app=sio_app)

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host=FASTAPI_HOST, port=FASTAPI_PORT_NUMBER)
