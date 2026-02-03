from fastapi import FastAPI
from fastapi_open_weather.app import router

app = FastAPI()

app.include_router(router)

