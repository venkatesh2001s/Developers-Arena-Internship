import requests
import json
from datetime import datetime, timedelta
from pathlib import Path
import time
from typing import Optional, Dict, Any, List    
from collections import defaultdict

# ==============================================================================
# FALLBACK FOR MISSING 'colorama' LIBRARY
# If colorama is not installed, the application defines dummy classes to prevent 
# a ModuleNotFoundError and runs successfully without terminal colors.
# ==============================================================================
try:
    from colorama import Fore, Style, init
    init(autoreset=True)
except ImportError:
    class DummyColor:
        def __getattr__(self, name):
            return ''
    
    class DummyStyle:
        def __getattr__(self, name):
            return ''

    Fore = DummyColor()
    Style = DummyColor()
    def init(autoreset=True):
        pass
    print("WARNING: 'colorama' not found. Running without terminal colors.")
# End of colorama fallback block
# ==============================================================================


# ==============================================================================
# 0. CONFIGURATION & API KEY
# NOTE: Replace this placeholder with your actual OpenWeatherMap API key.
# ==============================================================================
# 🎯 EXAMPLE: I have added a sample key structure here. Replace this!
OPENWEATHER_API_KEY = "af7d9a1704d9bfafd46b79c71a4dda29" 

if OPENWEATHER_API_KEY == "YOUR_API_KEY_HERE":
    print(Fore.RED + "WARNING: Please replace 'YOUR_API_KEY_HERE' with a valid OpenWeatherMap API key.")

# Cache duration set to 15 minutes (900 seconds)
CACHE_DURATION = 900 

# ==============================================================================
# 1. API CLIENT MODULE (Task 3 & Caching)
# ==============================================================================

class WeatherAPI:
    """Handles all weather API interactions with caching and error handling."""
    
    def __init__(self, api_key: str, base_url: str = "http://api.openweathermap.org/data/2.5"):
        self.api_key = api_key
        self.base_url = base_url
        self.cache_dir = Path("data/cache")
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self.cache_duration = CACHE_DURATION
        
    def _get_cached_data(self, cache_key: str) -> Optional[Dict]:
        """Get data from cache if valid"""
        cache_file = self.cache_dir / f"{cache_key}.json"
        
        if cache_file.exists():
            try:
                # Check if cache is still valid
                cache_time = cache_file.stat().st_mtime
                cache_age = time.time() - cache_time
                if cache_age < self.cache_duration:
                    with open(cache_file, 'r') as f:
                        data = json.load(f)
                        data['cache_age'] = cache_age # Inject cache age for display
                        return data
            except Exception as e:
                # print(f"Cache read error: {e}") # Debugging
                pass
        return None
    
    def _save_to_cache(self, cache_key: str, data: Dict):
        """Save data to cache"""
        cache_file = self.cache_dir / f"{cache_key}.json"
        try:
            with open(cache_file, 'w') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            # print(f"Cache write error: {e}") # Debugging
            pass
    
    def _make_request(self, endpoint: str, params: Dict, cache_key: str) -> Optional[Dict]:
        """Make API request with error handling and caching logic"""
        
        # 1. Check cache first
        cached_data = self._get_cached_data(cache_key)
        if cached_data:
            print(Fore.GREEN + f"API Status: Using cached data ({int(cached_data['cache_age'] / 60)} min old)")
            return cached_data
        
        # 2. Make live request
        print(Fore.YELLOW + "API Status: Fetching live data...")
        try:
            params['appid'] = self.api_key
            params['units'] = 'metric'  # Always request metric, parser will convert later
            
            response = requests.get(
                f"{self.base_url}/{endpoint}",
                params=params,
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                self._save_to_cache(cache_key, data)
                return data
            
            # Error Handling (Task 3)
            elif response.status_code == 401:
                print(Fore.RED + "Error: Invalid API key. Check API configuration.")
            elif response.status_code == 404:
                print(Fore.RED + "Error: City not found")
            elif response.status_code == 429:
                print(Fore.RED + "Error: API rate limit exceeded.")
            else:
                print(Fore.RED + f"Error: API request failed with status {response.status_code}")
                
        except requests.exceptions.Timeout:
            print(Fore.RED + "Error: Request timed out")
        except requests.exceptions.ConnectionError:
            print(Fore.RED + "Error: Network connection error.")
        except Exception as e:
            print(Fore.RED + f"An unexpected error occurred: {e}")
            
        return None
    
    def get_current_weather(self, city: str, country_code: str = None) -> Optional[Dict]:
        """Get current weather for a city"""
        query = city
        if country_code:
            query = f"{city},{country_code}"
        
        cache_key = f"current_{city}_{country_code}".replace(' ', '_')
        params = {'q': query}
        return self._make_request("weather", params, cache_key)

    def get_forecast(self, city: str, country_code: str = None) -> Optional[Dict]:
        """Get 5-day/3-hour forecast for a city"""
        query = city
        if country_code:
            query = f"{city},{country_code}"
            
        cache_key = f"forecast_{city}_{country_code}".replace(' ', '_')
        params = {'q': query}
        return self._make_request("forecast", params, cache_key)


# ==============================================================================
# 2. DATA PROCESSING MODULE (Task 4)
# ==============================================================================

class WeatherParser:
    """Parses raw JSON data into a structured format and handles conversions."""

    def __init__(self, unit: str = 'C'):
        self.unit = unit
        self.condition_icons = {
            'Clear': '☀️',
            'Clouds': '☁️',
            'Rain': '🌧️',
            'Drizzle': '🌦️',
            'Thunderstorm': '⛈️',
            'Snow': '❄️',
            'Mist': '🌫️',
            'Smoke': '🌫️',
            'Haze': '🌫️',
            'Dust': '💨',
            'Fog': '🌫️',
            'Sand': '💨',
            'Ash': '💨',
            'Squall': '🌬️',
            'Tornado': '🌪️',
        }

    def _c_to_f(self, temp_c: float) -> float:
        """Converts Celsius to Fahrenheit."""
        return (temp_c * 9/5) + 32

    def _convert_temp(self, temp_c: float) -> float:
        """Applies unit conversion based on self.unit."""
        if self.unit == 'F':
            return round(self._c_to_f(temp_c))
        return round(temp_c)

    def parse_current_weather(self, data: Dict[str, Any]) -> Optional[Dict]:
        """Parses current weather JSON."""
        if not data or 'main' not in data:
            return None
        
        # Get weather details
        temp_c = data['main']['temp']
        feels_like_c = data['main']['feels_like']
        
        # Format times
        sunrise = datetime.fromtimestamp(data['sys']['sunrise']).strftime('%H:%M')
        sunset = datetime.fromtimestamp(data['sys']['sunset']).strftime('%H:%M')
        last_updated = datetime.fromtimestamp(data.get('dt', time.time())).strftime('%Y-%m-%d %H:%M:%S')

        # Get main condition and description
        main_condition = data['weather'][0]['main']
        condition_desc = data['weather'][0]['description'].capitalize()
        icon = self.condition_icons.get(main_condition, '❓')

        return {
            'location': f"{data['name']}, {data['sys']['country']}",
            'last_updated': last_updated,
            'temp': self._convert_temp(temp_c),
            'temp_unit': self.unit,
            'feels_like': self._convert_temp(feels_like_c),
            'condition': f"{condition_desc} {icon}",
            'humidity': data['main']['humidity'],
            'wind_speed_kmh': round(data['wind']['speed'] * 3.6), # m/s to km/h
            'pressure': data['main']['pressure'],
            'visibility_km': round(data.get('visibility', 0) / 1000), # m to km
            'sunrise': sunrise,
            'sunset': sunset,
            'cache_age': data.get('cache_age'),
        }

    def parse_forecast(self, data: Dict[str, Any]) -> Optional[List[Dict]]:
        """Parses 5-day/3-hour forecast into daily summaries."""
        if not data or 'list' not in data:
            return None

        daily_data = defaultdict(lambda: {
            'temps': [], 'humidity': [], 'conditions': [], 'min_temp': float('inf'), 'max_temp': float('-inf')
        })

        # Process the 3-hour list
        for item in data['list']:
            dt_object = datetime.fromtimestamp(item['dt'])
            date_key = dt_object.date()

            temp = item['main']['temp']
            
            daily_data[date_key]['temps'].append(temp)
            daily_data[date_key]['humidity'].append(item['main']['humidity'])
            daily_data[date_key]['conditions'].append(item['weather'][0]['main'])
            
            # Update min/max across all 3-hour slots
            daily_data[date_key]['min_temp'] = min(daily_data[date_key]['min_temp'], item['main']['temp_min'])
            daily_data[date_key]['max_temp'] = max(daily_data[date_key]['max_temp'], item['main']['temp_max'])

        # Structure the final 5-day forecast
        forecast_list = []
        for date_key, day_data in sorted(daily_data.items())[:5]: # Take only the next 5 days
            
            # Get the most frequent condition (simple mode)
            condition_counts = defaultdict(int)
            for cond in day_data['conditions']:
                condition_counts[cond] += 1
            most_frequent_condition = max(condition_counts, key=condition_counts.get)
            icon = self.condition_icons.get(most_frequent_condition, '❓')
            
            # Calculate average humidity
            avg_humidity = round(sum(day_data['humidity']) / len(day_data['humidity']))

            forecast_list.append({
                'day': date_key.strftime('%a %d %b'),
                'icon': icon,
                'min': self._convert_temp(day_data['min_temp']),
                'max': self._convert_temp(day_data['max_temp']),
                'unit': self.unit,
                'condition': most_frequent_condition,
                'avg_humidity': avg_humidity,
            })

        return forecast_list

# ==============================================================================
# 3. DISPLAY MODULE (Task 5)
# ==============================================================================

class WeatherDisplay:
    """Formats and prints weather data to the console with colors and ASCII art."""

    def __init__(self, parser: WeatherParser):
        self.parser = parser

    def _get_temp_color(self, temp: float, unit: str) -> str:
        """Returns color based on temperature."""
        thresholds = {'C': (0, 25), 'F': (32, 77)} # Cold, Mild, Hot thresholds
        cold, hot = thresholds[unit]

        if temp < cold:
            return Fore.BLUE  # Cold
        elif temp > hot:
            return Fore.RED    # Hot
        else:
            return Fore.YELLOW + Style.BRIGHT # Mild/Warm

    def display_current_weather(self, current_data: Dict):
        """Prints formatted current weather data."""
        unit = current_data['temp_unit']
        temp_color = self._get_temp_color(current_data['temp'], unit)
        
        # Display cache status if available
        cache_age_sec = current_data.get('cache_age')
        cache_msg = ""
        if cache_age_sec is not None:
            cache_minutes = int(cache_age_sec / 60)
            cache_msg = f"(Cached: {cache_minutes} min old)"
        
        print("\n" + "="*50)
        print(Fore.CYAN + Style.BRIGHT + "🌤️  WEATHER DASHBOARD")
        print("="*50)
        
        print(f"📍 Current Location: {Fore.YELLOW}{current_data['location']}{Style.RESET_ALL}")
        print(f"🕐 Last Updated: {current_data['last_updated']} {cache_msg}\n")
        
        print(Fore.WHITE + "Current Weather:")
        print("────────────────")
        print(f"Temperature:   {temp_color}{current_data['temp']}°{unit} ({Style.RESET_ALL}Feels like: {self._get_temp_color(current_data['feels_like'], unit)}{current_data['feels_like']}°{unit}{Style.RESET_ALL})")
        print(f"Conditions:    {current_data['condition']}")
        print(f"Humidity:      {current_data['humidity']}%")
        print(f"Wind:          {current_data['wind_speed_kmh']} km/h")
        print(f"Pressure:      {current_data['pressure']} hPa")
        print(f"Visibility:    {current_data['visibility_km']} km")
        print(f"Sunrise:       {current_data['sunrise']}")
        print(f"Sunset:        {current_data['sunset']}")

    def display_forecast(self, forecast_data: List[Dict]):
        """Prints formatted 5-day forecast."""
        if not forecast_data:
            return
            
        unit = forecast_data[0]['unit']
        
        print("\n" + Fore.WHITE + "5-Day Forecast:")
        print("───────────────")
        
        for day in forecast_data:
            max_temp_color = self._get_temp_color(day['max'], unit)
            min_temp_color = self._get_temp_color(day['min'], unit)

            print(f"{Fore.CYAN}{day['day']}: "
                  f"{day['icon']}  "
                  f"{max_temp_color}{day['max']}°{unit} "
                  f"{Style.RESET_ALL}/ "
                  f"{min_temp_color}{day['min']}°{unit}{Style.RESET_ALL}  "
                  f"(Humidity: {day['avg_humidity']}%)")

# ==============================================================================
# 4. USER INTERFACE & MAIN LOGIC (Task 6)
# ==============================================================================

class WeatherApp:
    """Main application logic and user interface."""
    
    def __init__(self, api_key: str, default_city: str = "London"):
        self.api = WeatherAPI(api_key)
        self.parser = WeatherParser(unit='C') # Start with Celsius
        self.display = WeatherDisplay(self.parser)
        self.current_city = default_city
        self.favorites = {'London': 'GB', 'Paris': 'FR', 'Tokyo': 'JP'}
        
    def _fetch_and_display(self, city: str):
        """Fetches and displays both current weather and forecast."""
        
        # 1. Fetch Current Weather
        current_json = self.api.get_current_weather(city)
        if not current_json:
            return
        
        current_data = self.parser.parse_current_weather(current_json)
        if current_data:
            self.current_city = current_data['location']
            self.display.display_current_weather(current_data)
        
        # 2. Fetch Forecast
        forecast_json = self.api.get_forecast(city)
        if not forecast_json:
            return
            
        forecast_data = self.parser.parse_forecast(forecast_json)
        if forecast_data:
            self.display.display_forecast(forecast_data)

    def _set_units(self, unit: str):
        """Switches display units between C and F."""
        unit = unit.upper()
        if unit in ['C', 'F']:
            self.parser.unit = unit
            print(Fore.GREEN + f"\nUnits set to: {unit}ahrenheits" if unit == 'F' else f"\nUnits set to: {unit}elsius")
            self._fetch_and_display(self.current_city.split(',')[0].strip())
        else:
            print(Fore.RED + "Invalid unit. Use 'C' or 'F'.")

    def _show_favorites(self):
        """Displays saved favorite cities."""
        print("\n" + Fore.YELLOW + "⭐ Favorite Cities:")
        if not self.favorites:
            print(Fore.WHITE + "No favorites saved.")
            return

        for i, (city, code) in enumerate(self.favorites.items()):
            print(f" {i+1}. {city}, {code}")
        
    def _help(self):
        """Displays command help."""
        print("\n" + Fore.CYAN + "Available Commands:")
        print("-" * 20)
        print(Fore.YELLOW + "search [city name]" + Fore.WHITE + " - Search for a new city (e.g., search Tokyo)")
        print(Fore.YELLOW + "units [C/F]" + Fore.WHITE + "    - Switch temperature units (e.g., units F)")
        print(Fore.YELLOW + "refresh" + Fore.WHITE + "        - Refresh data for the current city")
        print(Fore.YELLOW + "favs" + Fore.WHITE + "           - Show favorite cities")
        print(Fore.YELLOW + "help" + Fore.WHITE + "           - Show this help menu")
        print(Fore.YELLOW + "quit" + Fore.WHITE + "           - Exit the application")
        
    def run(self):
        """Main application loop."""
        print(Fore.GREEN + Style.BRIGHT + "Welcome to the Python Weather Dashboard!")
        self._help()
        
        # Initial fetch
        self._fetch_and_display(self.current_city)
        
        while True:
            try:
                command = input(Fore.YELLOW + f"\n{self.current_city} [{self.parser.unit}]: " + Style.RESET_ALL).strip().lower()
                
                if command == 'quit':
                    print(Fore.CYAN + "Goodbye!")
                    break
                elif command == 'refresh':
                    self._fetch_and_display(self.current_city.split(',')[0].strip())
                elif command.startswith('search '):
                    new_city = command[7:].strip()
                    if new_city:
                        self._fetch_and_display(new_city)
                    else:
                        print(Fore.RED + "Please specify a city name.")
                elif command.startswith('units '):
                    unit = command[6:].strip()
                    self._set_units(unit)
                elif command == 'favs':
                    self._show_favorites()
                elif command == 'help':
                    self._help()
                elif command:
                    print(Fore.RED + f"Unknown command: '{command}'. Type 'help' for commands.")

            except KeyboardInterrupt:
                print(Fore.CYAN + "\nGoodbye!")
                break
            except Exception as e:
                print(Fore.RED + f"An internal error occurred: {e}")


# ==============================================================================
# ENTRY POINT
# ==============================================================================

if __name__ == "__main__":
    # --- IMPORTANT: Replace the dummy key here with your actual key ---
    if OPENWEATHER_API_KEY == "YOUR_API_KEY_HERE":
        print(Fore.RED + "Please replace the API key placeholder before running.")
    else:
        app = WeatherApp(api_key=OPENWEATHER_API_KEY, default_city="New York")
        app.run()