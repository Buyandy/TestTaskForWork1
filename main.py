from fastapi import FastAPI
from open_weather_fastapi.routers import router_main
from open_weather_fastapi.core import lifespan

app = FastAPI(lifespan=lifespan)

app.include_router(router_main)

