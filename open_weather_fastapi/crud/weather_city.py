from sqlalchemy.orm import Session, sessionmaker
from ..models import *
from api_open_weather.schemas import CurrentWeather


SessionLocal = sessionmaker(engine)


    

def add_city(name: str, latitude: float, longitude: float, db: Session, current_weather: CurrentWeather) -> Cities:
    city = Cities(
        name=name,
        latitude=latitude,
        longitude=longitude,
        weather = Weathers(
            temperature_2m=current_weather.temperature_2m,
            relative_humidity_2m=current_weather.relative_humidity_2m,
            pressure_msl=current_weather.pressure_msl,
            surface_pressure=current_weather.surface_pressure,
        )
    )
    db.add(city)
    db.commit()
    db.refresh(city)
    return city