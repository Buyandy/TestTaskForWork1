from fastapi import FastAPI
from open_weather_fastapi.routers import router_main

app = FastAPI()

app.include_router(router_main)

