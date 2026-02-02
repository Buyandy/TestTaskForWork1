import openmeteo_requests
import asyncio

from openmeteo_sdk.WeatherApiResponse import WeatherApiResponse


class Coordinate:
    width: float
    length: float

    def __init__(self, latitude: float, longitude: float) -> None:
        self.width = latitude
        self.length = longitude



class CurrentWeather:
    coordinate: Coordinate
    temperature_2m: float | None
    relative_humidity_2m: float | None
    pressure_msl: float | None
    surface_pressure: float | None

    def __init__(self, latitude: float, longitude: float, temperature_2m: float | None = None,
    relative_humidity_2m: float | None = None, pressure_msl: float | None = None,
    surface_pressure: float | None = None
    ) -> None:
        self.coordinate = Coordinate(latitude=latitude, longitude=longitude)
        self.temperature_2m = temperature_2m
        self.relative_humidity_2m = relative_humidity_2m
        self.pressure_msl = pressure_msl
        self.surface_pressure = surface_pressure



async def _get_response_weather(latitude: float, longitude: float) -> WeatherApiResponse | None:
    openmeteo = openmeteo_requests.AsyncClient()

    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "current": ["temperature_2m", "relative_humidity_2m", "pressure_msl", "surface_pressure"],
    }
    responses = await openmeteo.weather_api(url, params=params)

    response = responses[0]
    if WeatherApiResponse is response:
        return response
    return None


async def get_current_weather(latitude: float, longitude: float) -> CurrentWeather | None:
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



if __name__ == "__main__":
    asyncio.run(get_current_weather(52.52, 13.41))