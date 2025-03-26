import os
import json
import requests
from typing import Optional

from agents import function_tool

OPEN_WEATHER_API_KEY = os.environ.get('OPEN_WEATHER_API_KEY')

def get_coordinates(location: str) -> Optional[dict[str, int]]:
    url = f'http://api.openweathermap.org/geo/1.0/direct?q={location}&limit=1&appid={OPEN_WEATHER_API_KEY}'

    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        data = data[0]
        return {"lat": data['lat'], "lon": data['lon']}
    
    return None

@function_tool
def get_current_weather(location: str):
    """
    Get the current weather for a given location.

    Args:
        location (str): The name of the location.

    Returns:
        str: A JSON object containing the current weather data.
        str: A message indicating if the location was not found.
    """
    coordinates = get_coordinates(location)
    if coordinates is None:
        return "Location not found."
    
    lat, long = coordinates['lat'], coordinates['lon']
    url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={long}&appid={OPEN_WEATHER_API_KEY}"

    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return json.dumps(data)
    
    return "the given location not found"

# response = get_current_weather("Lahore, Pakistan")
# print(response)