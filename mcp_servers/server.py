from mcp.server.fastmcp import FastMCP
from typing_extensions import Any
import httpx

from dotenv import load_dotenv
import requests

load_dotenv("../.env")

mcp = FastMCP(name="My_Server", host="0.0.0.0", port=8040)


async def make_nws_request(url: str) -> dict[str, Any] | None:
    """Make a request to the NWS API with proper error handling."""
    headers = {
        "User-Agent": "",
        "Accept": ""
    }
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, headers=headers, timeout=30.0)
            response.raise_for_status()
            return response.json()
        except Exception:
            return None

def format_alert(feature: dict) -> str:
    """Format an alert feature into a readable string."""
    props = feature ["properties"]
    return f"""
    Event: {(props.get('event', 'Unknown'))}
    Area: {props.get('areaDesc', 'Unknown')}
    Severity: {props.get('severity', 'Unknown')}
    Description: {props.get('description', 'No description available')}
    Instructions
    """
@mcp.tool()
async def get_alerts(state: str) -> str:
    """Get weather alerts for a US state.
    Args:
    state: Two-letter US state code (e.g. CA, NY)
    """
    url = f" {NWS_API_BASE}/alerts/active/area/{state}"
    data = await make_nws_request(url)
    if not data or "features" not in data:
        return "Unable to fetch alerts or no alerts found."
    if not data["features"]:
        return "No active alerts for this state."
    alerts = [format_alert(feature) for feature in data["features"]]
    return {"Weather Alerts":"\n--\n".join(alerts)}

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
    return {"result":a + b}

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
    return {"result": a * b}


@mcp.tool()
async def get_weather_from_weatherapi(city: str, WEATHER_API_KEY: str)-> str: #
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

        return {"Weather Report":report}

    except Exception as e:
        return f"❗ Error: {str(e)}"
    
# Add a dynamic greeting resource
@mcp.resource("greeting://{name}")
def get_greeting(name: str) -> str:
    """Get a personalized greeting"""
    return f"Hello, {name}!"


# Add a prompt
@mcp.prompt()
def greet_user(name: str, style: str = "friendly") -> str:
    """Generate a greeting prompt"""
    styles = {
        "friendly": "Please write a warm, friendly greeting",
        "formal": "Please write a formal, professional greeting",
        "casual": "Please write a casual, relaxed greeting",
    }

    return f"{styles.get(style, styles['friendly'])} for someone named {name}."

from PIL import Image as PILImage

from mcp.server.fastmcp import FastMCP, Image

@mcp.tool()
def create_thumbnail(image_path: str) -> Image:
    """Create a thumbnail from an image"""
    img = PILImage.open(image_path)
    img.thumbnail((100, 100))
    return Image(data=img.tobytes(), format="png")

if __name__ == "__main__":
    print("🚀 Starting MCP Server...")
    mcp.run(transport="stdio") # stdio streamable-http

# cd mcp_servers
# mcp dev server.py
