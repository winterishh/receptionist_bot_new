from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from routes.ask import router as ask_router
from routes.display import router as display_router


app = FastAPI()


app.mount(
    "/static",
    StaticFiles(directory="static"),
    name="static"
)


app.include_router(ask_router)
app.include_router(display_router)