from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from api_open_weather.schemas import CurrentWeather
from api_open_weather.open_weather import get_current_weather
from .. import crud


def get_db():
    db = crud.SessionLocal()
    try:
        yield db
    finally:
        db.close()


router_app = APIRouter()


@router_app.get("/current_weather/", response_model=CurrentWeather)
async def current_weather(longitude: float | None,latitude: float | None):
    if longitude and latitude:
        if current_weather := await get_current_weather(latitude=latitude, longitude=longitude):
            return current_weather
    raise HTTPException(status_code=404, detail="Результаты не найдены!")

@router_app.get("/add_city/")
async def add_city(name: str, latitude: float, longitude: float, db: Session =Depends(get_db)):
    if longitude and latitude:
        if current_weather := await get_current_weather(latitude=latitude, longitude=longitude):
            return crud.add_city(name=name, latitude=latitude, longitude=longitude, db=db, current_weather=current_weather)
    raise HTTPException(status_code=404)