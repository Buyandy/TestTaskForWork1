from contextlib import contextmanager
from typing import Generator
from niquests import get
from sqlalchemy.orm import Session, sessionmaker
from ..models import Cities, Weathers
from api_open_weather.schemas import CurrentWeather
from api_open_weather.open_weather import get_current_weather
from sqlalchemy import func, and_
from ..core import engine
import logging
from ..tools.get_time import now_time


logger = logging.getLogger("uvicorn.access")

SessionLocal = sessionmaker(engine)

@contextmanager
def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
        db.commit()
    except Exception as e:
        db.rollback()
        logger.error(f"Ошибка транзакции: {e}")
        raise
    finally:
        db.close()
    

def add_city(name: str, latitude: float, longitude: float, db: Session, current_weather: CurrentWeather) -> Cities:
    existing_city = db.query(Cities).filter(
        (Cities.name == name) | 
        and_(func.abs(Cities.latitude - latitude) < 0.001, func.abs(Cities.longitude - longitude) < 0.001)
    ).first()
    
    if existing_city:
        update_weather(existing_city, current_weather, db)
        return existing_city
    
    return create_new_city(name, latitude, longitude, current_weather, db)


def update_weather(city: Cities, weather: CurrentWeather, db: Session):
    logger.info(city.weather.updated_at)
    if city.weather:
        city.weather.temperature_2m = weather.temperature_2m
        city.weather.relative_humidity_2m = weather.relative_humidity_2m
        city.weather.pressure_msl = weather.pressure_msl
        city.weather.surface_pressure = weather.surface_pressure
        city.weather.updated_at = now_time()
    else:
        city.weather = Weathers(
            temperature_2m=weather.temperature_2m,
            relative_humidity_2m=weather.relative_humidity_2m,
            pressure_msl=weather.pressure_msl,
            surface_pressure=weather.surface_pressure,
            created_at=now_time(),
            updated_at=now_time()  
        )
    db.commit()
    db.refresh(city, ["weather"])
    logger.info(f"Погода в городе {city.name} успешно обновленна!")
    logger.info(city.weather.updated_at)

def create_new_city(name: str, latitude: float, longitude: float, weather: CurrentWeather, db: Session) -> Cities:
    city = Cities(
        name=name,
        latitude=latitude,
        longitude=longitude,
        weather=Weathers(
            temperature_2m=weather.temperature_2m,
            relative_humidity_2m=weather.relative_humidity_2m,
            pressure_msl=weather.pressure_msl,
            surface_pressure=weather.surface_pressure,
        )
    )
    db.add(city)
    db.commit()
    db.refresh(city)
    logger.info(f"Добавлен новый город с названием {city.name}")
    return city

async def update_all_weather():
    with get_db() as db:
        if cities := db.query(Cities).all():
            for city in cities:
                if current_weather := await get_current_weather(latitude=city.latitude, longitude=city.longitude):#type:ignore
                    update_weather(city, current_weather, db)
                
