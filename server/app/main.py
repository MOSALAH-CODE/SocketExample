from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import engine
from models import Base
from sockets import sio_app
from utilities.config_variables import FASTAPI_HOST, FASTAPI_PORT_NUMBER
from routers import players, groups, levels

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(levels.router)
app.include_router(groups.router)
app.include_router(players.router)

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
