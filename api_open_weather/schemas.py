from pydantic import BaseModel

class CurrentWeather(BaseModel):
    longitude: float
    latitude: float
    temperature_2m: float | None = None
    relative_humidity_2m: float | None = None
    pressure_msl: float | None = None
    surface_pressure: float | None = None
    wind_speed_10m: float | None = None
    precipitation: float | None = None


       
