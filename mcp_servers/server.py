from mcp.server.fastmcp import FastMCP
from dotenv import load_dotenv
import requests

load_dotenv("../.env")

mcp = FastMCP(
    name="My_Server",
    host = "0.0.0.0",
    port = 8040,
)

@mcp.tool()
async def aadd(a: float, b: float)-> float:
    """
    Two numbers are added together
    Args:
        a (float) : first argument in the function
        b (float) : second argument in the function
    Returns:
        c (float): addition of two values
    """
    return a + b

@mcp.tool()
async def amultiply(a: float, b: float)-> float:
    """
    Two numbers are multiplied together
    Args:
        a (float) : first argument in the function
        b (float) : second argument in the function
    Returns:
        c (float): addition of two values
    """
    return a * b


@mcp.tool()
async def get_weather_from_weatherapi(city: str, WEATHER_API_KEY: str)-> str:
    """
    Returns weather data prediction for next 3 days
    Args:
        city (str) : name ofthe city to check weather
        WEATHER_API_KEY (str) : app key to establish connection
    Returns:
        str: prediction of weather for next 3 days
    """
    # def get_weather_from_weatherapi() :
    try:
        url = f"http://api.weatherapi.com/v1/forecast.json?key={WEATHER_API_KEY}&q={city}&days=3&aqi=no&alerts=no"
        response = requests.get(url)
        
        # Ensure valid JSON
        if response.status_code != 200:
            return f"❗ API request failed with status code {response.status_code}"
        
        data = response.json()

        if "error" in data:
            return f"❗ API Error: {data['error'].get('message', 'Unknown error')}"

        location = data["location"]
        current = data["current"]
        forecast = data["forecast"]["forecastday"]

        report = (
            f"📍 {location['name']}, {location['country']}\n"
            f"🌡️ Temp: {current['temp_c']}°C (Feels like {current['feelslike_c']}°C)\n"
            f"💧 Humidity: {current['humidity']}% | ☁️ Cloud: {current['cloud']}%\n"
            f"🌬️ Wind: {current['wind_kph']} kph\n"
            f"🌤️ Condition: {current['condition']['text']}\n\n"
            f"🗓️ Forecast:\n"
        )

        for day in forecast:
            date = day["date"]
            day_data = day["day"]
            report += (
                f"{date}: 🌡️ {day_data['avgtemp_c']}°C, 🌧️ {day_data['condition']['text']}, "
                f"💧 Humidity: {day_data['avghumidity']}%, 🌬️ Wind: {day_data['maxwind_kph']} kph\n"
            )

        return report

    except Exception as e:
        return f"❗ Error: {str(e)}"

if __name__ == "__main__":
    print("🚀 Starting MCP Server...")
    mcp.run(transport="stdio") # stdio Streamable_htpp

# cd mcp_servers
# mcp dev server.py
