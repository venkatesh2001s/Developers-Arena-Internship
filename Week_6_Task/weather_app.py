import requests

def get_weather(city, api_key):
    url = "https://api.openweathermap.org/data/2.5/weather"
    params = {"q": city, "appid": api_key, "units": "metric"}
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        
        temp = data["main"]["temp"]
        desc = data["weather"][0]["description"]
        print(f"Weather in {city}:\nTemperature: {temp}°C\nConditions: {desc.capitalize()}")
    except requests.exceptions.HTTPError as e:
        print(f"HTTP error occurred: {e}")
    except Exception as e:
        print(f"Failed to get weather data: {e}")

if __name__ == "__main__":
    city = input("Enter city name: ")
    api_key = "e7c39f58087f9f2fdac43dc7d73f15c7"  # Replace with your OpenWeatherMap API key
    get_weather(city, api_key)
