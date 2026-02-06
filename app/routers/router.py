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

@router_app.post("/add_city/", status_code=201)
async def add_city(name: str, latitude: float, longitude: float, db: Session =Depends(get_db)):
    if longitude and latitude:
        if current_weather := await get_current_weather(latitude=latitude, longitude=longitude):
            return crud.add_city(name=name, latitude=latitude, longitude=longitude, db=db, current_weather=current_weather)
    raise HTTPException(status_code=400)


@router_app.get("/all_cities/")
async def all_cities(db: Session = Depends(get_db)):
    if names := crud.get_all_name_cities(db):
        return names
    return "В данный момент городов нету"


@router_app.get("/hourly_weather/{name_city}-{hour}")
async def hourly_weather(
    name_city: str,
    hour: int,
    get_temperature: bool = False,
    get_humidity: bool = False,
    get_wind_speed: bool = False,
    get_precipitation: bool = False,
    db: Session = Depends(get_db)
    ):
    if name_city and hour:
        if hour > 23 or hour < 0:
            return HTTPException(status_code=400, detail="Часы неправильно заданы!")

        if get_temperature or get_humidity or get_wind_speed or get_precipitation:
            if hour_weather := await crud.get_current_info_weather(
                name_city=name_city,
                hour=hour,
                get_temperature=get_temperature,
                get_humidity=get_humidity,
                get_wind_speed=get_wind_speed,
                get_precipitation=get_precipitation,
                db=db
            ):
                return hour_weather
            else:
                return HTTPException(status_code=404, detail="Город не найден!")
        else:
            if hour_weather := await crud.get_all_hourly_weather(db, name_city, hour):
                return hour_weather
            return HTTPException(status_code=404, detail="Город не найден!")
    return HTTPException(status_code=400, detail="Неполный запрос!")