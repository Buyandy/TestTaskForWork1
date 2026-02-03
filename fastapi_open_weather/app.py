from fastapi import APIRouter, HTTPException
from api_open_weather.types import CurrentWeather
from api_open_weather.open_weather import get_current_weather



router = APIRouter()


@router.get("/current_weather/", response_model=CurrentWeather)
async def current_weather(longitude: float | None,latitude: float | None):
    if longitude and latitude:
        if current_weather := await get_current_weather(latitude=latitude, longitude=longitude):
            return current_weather
    raise HTTPException(status_code=404, detail="Результаты не найдены!")