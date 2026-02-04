from pydantic import BaseModel

class CurrentWeather(BaseModel):
    longitude: float
    latitude: float
    temperature_2m: float | None
    relative_humidity_2m: float | None
    pressure_msl: float | None
    surface_pressure: float | None