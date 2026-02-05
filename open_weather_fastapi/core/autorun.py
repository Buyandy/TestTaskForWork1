from contextlib import asynccontextmanager
from fastapi import FastAPI
from ..services import start_updater_weather, shutdown_updater_weather

import logging
logger = logging.getLogger("uvicorn.access")


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Запуск служб")
    if start_updater_weather():
        logger.info("Служба start_updater_weather успешно запущенна!")
    else:
        logger.error("Служба start_updater_weather не удалось запустить!")
    
    yield

    if shutdown_updater_weather:
        logger.info("Служба start_updater_weather успешно остановлена!")
    else:
        logger.error("Служба start_updater_weather не удалось остановить!")



