import openmeteo_requests
import asyncio

from openmeteo_sdk.WeatherApiResponse import WeatherApiResponse
from .schemas import CurrentWeather





async def _get_response_weather(latitude: float, longitude: float, get_hourly = False) -> WeatherApiResponse | None:
    openmeteo = openmeteo_requests.AsyncClient()

    url = "https://api.open-meteo.com/v1/forecast"
    if get_hourly:
        params = {
        "latitude": latitude,
        "longitude": longitude,
        "hourly": [
            "temperature_2m",           
            "relative_humidity_2m",     
            "wind_speed_10m",           
            "precipitation"
        ],
        "timezone": "auto"
    }
    else:
        params = {
            "latitude": latitude,
            "longitude": longitude,
            "current": ["temperature_2m", "relative_humidity_2m", "pressure_msl", "surface_pressure"],
        }
    responses = await openmeteo.weather_api(url, params=params)

    response = responses[0]
    if response:
        return response
    return None


async def get_current_weather(latitude: float, longitude: float) -> CurrentWeather | None:

    if (abs(latitude) > 90) or (abs(longitude) > 180):
        return None

    if response := await _get_response_weather(latitude, longitude):
        if current := response.Current():
            if current_temperature_2m := current.Variables(0):                     #1
                current_temperature_2m = current_temperature_2m.Value()
            else:
                current_temperature_2m = None
            
            if current_relative_humidity_2m := current.Variables(1):               #2
                current_relative_humidity_2m = current_relative_humidity_2m.Value()
            else:
                current_relative_humidity_2m = None
            
            if current_pressure_msl := current.Variables(2):                       #3
                current_pressure_msl = current_pressure_msl.Value()
            else:
                current_pressure_msl = None
            
            if current_surface_pressure := current.Variables(3):                   #4
                current_surface_pressure = current_surface_pressure.Value()
            else:
                current_surface_pressure = None
            

            current_weather = CurrentWeather(
                latitude=latitude,
                longitude=longitude,
                temperature_2m=current_temperature_2m,
                relative_humidity_2m=current_relative_humidity_2m,
                pressure_msl=current_pressure_msl,
                surface_pressure=current_surface_pressure
            )
            return current_weather
    return None


async def get_hour_weather(latitude: float, longitude: float, hour: int) -> CurrentWeather | None:
    if response := await _get_response_weather(latitude=latitude, longitude=longitude, get_hourly=True):
        if hourly := response.Hourly():
            hourly_temperature_2m = hourly.Variables(0).ValuesAsNumpy()[hour] # type:ignore
            hourly_relative_humidity_2m = hourly.Variables(1).ValuesAsNumpy()[hour] # type:ignore 
            hourly_wind_speed_10m = hourly.Variables(2).ValuesAsNumpy()[hour]   # type:ignore
            hourly_precipitation = hourly.Variables(3).ValuesAsNumpy()[hour] # type:ignore
            
            return CurrentWeather(
                longitude=longitude,
                latitude=latitude,
                temperature_2m=hourly_temperature_2m,
                relative_humidity_2m=hourly_relative_humidity_2m,
                wind_speed_10m=hourly_wind_speed_10m,
                precipitation=hourly_precipitation
            )
    return None
    
            



if __name__ == "__main__":
    asyncio.run(get_hour_weather(52.52, 13.41, 12))