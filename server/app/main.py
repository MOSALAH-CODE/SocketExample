from fastapi import FastAPI, Request
from middleware import standard_response
from fastapi.middleware.cors import CORSMiddleware
from sockets import sio_app
from utilities.config_variables import FASTAPI_HOST, FASTAPI_PORT_NUMBER
from routers import leaderboard

app = FastAPI()

@app.middleware("http")
async def custom_middleware(request: Request, call_next):
    return await standard_response(request, call_next)

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
