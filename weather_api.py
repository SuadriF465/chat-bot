import requests
from config import API_KEY, BASE_URL

def get_weather(city: str):
    params = {
        "q": city,
        "appid": API_KEY,
        "units": "metric",
        "lang": "en"
    }

    try:
        response = requests.get(BASE_URL, params=params, timeout=5)
        response.raise_for_status()
        data = response.json()

        weather_data = {
            "temp": data["main"]["temp"],
            "feels_like": data["main"]["feels_like"],
            "humidity": data["main"]["humidity"],
            "description": data["weather"][0]["description"].capitalize(),
            "city_name": data["name"],
            "country": data["sys"]["country"]
        }
        return weather_data

    except requests.exceptions.HTTPError as http_err:
        if response.status_code == 404:
            return "404"  
        return None
    except requests.exceptions.RequestException:
        return None