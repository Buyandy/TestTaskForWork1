from fastapi import FastAPI
from app.routers import router_main
from app.core import lifespan

app = FastAPI(lifespan=lifespan)

app.include_router(router_main)

