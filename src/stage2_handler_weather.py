import os
import re
from typing import Optional
import requests


def _get_api_key() -> str:
    # 1) Environment variable
    key = os.getenv("OPENWEATHER_API_KEY", "")
    if key:
        return key
    # 2) Streamlit secrets (if running under Streamlit)
    try:
        import streamlit as st  # Lazy import; safe outside Streamlit too
        return st.secrets.get("OPENWEATHER_API_KEY", "")
    except Exception:
        return ""

OPENWEATHER_API_KEY = _get_api_key()


def extract_city(user_text: str) -> Optional[str]:
    """
    Very simple city extractor.
    Tries patterns like: weather in <city>, forecast for <city>, <city> weather.
    Fallback: last token if it looks like a word.
    """
    patterns = [
        r"weather in\s+([A-Za-z\s\-']+)",
        r"forecast in\s+([A-Za-z\s\-']+)",
        r"forecast for\s+([A-Za-z\s\-']+)",
        r"in\s+([A-Za-z\s\-']+)\s*(?:today|tomorrow|now)?",
        r"([A-Za-z\s\-']+)\s+weather",
    ]
    text = user_text.strip()
    for p in patterns:
        m = re.search(p, text, flags=re.IGNORECASE)
        if m:
            city = m.group(1).strip()
            city = re.sub(r"\s+", " ", city)
            if city:
                return city
    # fallback: last token if alphabetic
    tokens = re.findall(r"[A-Za-z\-']+", text)
    if tokens:
        return tokens[-1]
    return None


def fetch_weather(city: str) -> Optional[dict]:
    if not OPENWEATHER_API_KEY:
        return None
    try:
        params = {
            "q": city,
            "appid": OPENWEATHER_API_KEY,
            "units": "metric",
        }
        resp = requests.get("https://api.openweathermap.org/data/2.5/weather", params=params, timeout=8)
        if resp.status_code == 200:
            return resp.json()
        return None
    except Exception:
        return None


def format_weather(resp: dict, city_fallback: str) -> str:
    try:
        name = resp.get("name") or city_fallback
        main = resp.get("main", {})
        weather_list = resp.get("weather", [])
        desc = weather_list[0]["description"] if weather_list else "weather"
        temp = main.get("temp")
        feels = main.get("feels_like")
        humidity = main.get("humidity")
        pieces = []
        if temp is not None:
            pieces.append(f"{temp:.0f}°C")
        if feels is not None:
            pieces.append(f"feels {feels:.0f}°C")
        if humidity is not None:
            pieces.append(f"humidity {humidity}%")
        stats = ", ".join(pieces) if pieces else ""
        stats = f" ({stats})" if stats else ""
        return f"Weather in {name}: {desc}{stats}."
    except Exception:
        return f"Weather in {city_fallback}: (couldn't parse details)."


def handle_weather_request(user_text: str) -> str:
    city = extract_city(user_text) or "Singapore"
    data = fetch_weather(city)
    if data:
        return format_weather(data, city)
    if not OPENWEATHER_API_KEY:
        return (
            "To get live weather, set OPENWEATHER_API_KEY in your environment. "
            f"For example, PowerShell: $env:OPENWEATHER_API_KEY='YOUR_KEY'."
        )
    return f"I couldn't fetch weather for {city}. Try another city name."