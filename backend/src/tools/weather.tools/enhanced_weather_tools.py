"""
Enhanced Weather Tools - Multiple weather tools for comprehensive weather capabilities
Includes current weather, forecasts, climate data, and weather comparisons
"""

from langchain_core.tools import tool

@tool
def get_weather_info(city: str) -> str:
    """Get current weather information for a city.
    
    Args:
        city: Name of the city
        
    Returns:
        Current weather information for the city
    """
    # Mock weather data (in real app, would call actual weather API)
    weather_data = {
        "new york": "🌤️ Partly cloudy, 22°C, light breeze",
        "london": "🌧️ Rainy, 15°C, moderate wind", 
        "tokyo": "☀️ Sunny, 28°C, clear skies",
        "paris": "⛅ Overcast, 18°C, calm",
        "sydney": "🌞 Bright and sunny, 25°C, gentle breeze",
        "mumbai": "🌦️ Monsoon season, 26°C, heavy rain expected",
        "los angeles": "☀️ Sunny, 24°C, clear skies",
        "berlin": "⛅ Cloudy, 16°C, light wind",
        "moscow": "❄️ Snowy, -5°C, cold and crisp"
    }
    
    city_lower = city.lower()
    weather = weather_data.get(city_lower, f"🌍 Weather data for {city} not available in demo")
    
    print(f"🌤️ Weather tool used for: {city} → {weather}")
    return weather

@tool
def get_weather_forecast(city: str, days: int = 5) -> str:
    """Get multi-day weather forecast for a city.
    
    Args:
        city: Name of the city
        days: Number of days to forecast (default 5)
        
    Returns:
        Weather forecast for the specified number of days
    """
    print(f"📅 [WEATHER TOOL] Getting {days}-day forecast for {city}")
    
    # Mock forecast data
    forecast_templates = {
        "new york": [
            "Day 1: 🌤️ Partly cloudy, 22°C",
            "Day 2: ☀️ Sunny, 25°C", 
            "Day 3: 🌦️ Light rain, 18°C",
            "Day 4: ⛅ Cloudy, 20°C",
            "Day 5: ☀️ Clear skies, 24°C"
        ],
        "london": [
            "Day 1: 🌧️ Rainy, 15°C",
            "Day 2: ⛅ Overcast, 17°C",
            "Day 3: 🌦️ Drizzle, 14°C", 
            "Day 4: ☁️ Cloudy, 16°C",
            "Day 5: 🌤️ Partly sunny, 19°C"
        ],
        "tokyo": [
            "Day 1: ☀️ Sunny, 28°C",
            "Day 2: ☀️ Clear, 30°C",
            "Day 3: 🌤️ Partly cloudy, 26°C",
            "Day 4: ⛅ Overcast, 24°C", 
            "Day 5: ☀️ Sunny, 29°C"
        ]
    }
    
    city_lower = city.lower()
    forecast_data = forecast_templates.get(city_lower, [
        f"Day {i+1}: 🌍 Forecast for {city} not available" for i in range(days)
    ])
    
    limited_forecast = forecast_data[:min(days, len(forecast_data))]
    result = f"📅 {days}-day forecast for {city}:\n" + "\n".join(limited_forecast)
    
    print(f"📅 [WEATHER TOOL] Forecast generated for {city}")
    return result

@tool
def get_climate_data(city: str, month: str) -> str:
    """Get historical climate data for a city and month.
    
    Args:
        city: Name of the city
        month: Month name (e.g., 'January', 'July')
        
    Returns:
        Historical climate information for the city and month
    """
    print(f"📊 [WEATHER TOOL] Getting climate data for {city} in {month}")
    
    # Mock climate data
    climate_data = {
        ("new york", "january"): "❄️ Average: 2°C, Snow common, 10 rainy days",
        ("new york", "july"): "☀️ Average: 25°C, Warm and humid, 8 rainy days",
        ("london", "january"): "🌧️ Average: 7°C, Very wet, 15 rainy days", 
        ("london", "july"): "🌤️ Average: 18°C, Mild summer, 10 rainy days",
        ("tokyo", "january"): "☀️ Average: 6°C, Dry and clear, 5 rainy days",
        ("tokyo", "july"): "🌦️ Average: 26°C, Hot and humid, 12 rainy days",
        ("mumbai", "july"): "🌊 Average: 27°C, Monsoon season, 25 rainy days",
        ("mumbai", "january"): "☀️ Average: 24°C, Dry season, 1 rainy day"
    }
    
    key = (city.lower(), month.lower())
    climate_info = climate_data.get(key, f"📊 Climate data for {city} in {month} not available")
    
    result = f"📊 Climate data for {city} in {month}:\n{climate_info}"
    print(f"📊 [WEATHER TOOL] Climate data retrieved for {city}")
    return result

@tool
def compare_weather(city1: str, city2: str) -> str:
    """Compare current weather between two cities.
    
    Args:
        city1: First city to compare
        city2: Second city to compare
        
    Returns:
        Weather comparison between the two cities
    """
    print(f"⚖️ [WEATHER TOOL] Comparing weather: {city1} vs {city2}")
    
    # Get weather for both cities using the existing tool logic
    weather_data = {
        "new york": {"temp": 22, "condition": "Partly cloudy", "emoji": "🌤️"},
        "london": {"temp": 15, "condition": "Rainy", "emoji": "🌧️"}, 
        "tokyo": {"temp": 28, "condition": "Sunny", "emoji": "☀️"},
        "paris": {"temp": 18, "condition": "Overcast", "emoji": "⛅"},
        "sydney": {"temp": 25, "condition": "Sunny", "emoji": "🌞"},
        "mumbai": {"temp": 26, "condition": "Monsoon", "emoji": "🌦️"},
        "los angeles": {"temp": 24, "condition": "Sunny", "emoji": "☀️"},
        "berlin": {"temp": 16, "condition": "Cloudy", "emoji": "⛅"},
        "moscow": {"temp": -5, "condition": "Snowy", "emoji": "❄️"}
    }
    
    city1_data = weather_data.get(city1.lower())
    city2_data = weather_data.get(city2.lower())
    
    if not city1_data:
        return f"❌ Weather data for {city1} not available"
    if not city2_data:
        return f"❌ Weather data for {city2} not available"
    
    # Create comparison
    temp_diff = city1_data["temp"] - city2_data["temp"]
    temp_comparison = "warmer" if temp_diff > 0 else "cooler" if temp_diff < 0 else "same temperature as"
    
    result = f"""⚖️ Weather Comparison: {city1} vs {city2}

🌍 {city1}: {city1_data['emoji']} {city1_data['condition']}, {city1_data['temp']}°C
🌍 {city2}: {city2_data['emoji']} {city2_data['condition']}, {city2_data['temp']}°C

📊 Summary: {city1} is {abs(temp_diff)}°C {temp_comparison} {city2}
"""
    
    print(f"⚖️ [WEATHER TOOL] Comparison completed")
    return result 