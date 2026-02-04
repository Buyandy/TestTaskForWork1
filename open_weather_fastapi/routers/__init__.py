from fastapi import APIRouter
from .app import router_app



router_main = APIRouter()

router_main.include_router(router=router_app)