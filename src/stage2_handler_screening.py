import requests
import os
import re
from random import choice as choose
import urllib.parse

def _get_serpapi_key() -> str:
    key = os.getenv("SERPAPI_KEY", "")
    if key:
        return key
    try:
        import streamlit as st
        return st.secrets.get("SERPAPI_KEY", "")
    except Exception:
        return ""

def extract_movie_title(user_text: str):
    """
    Extracts the movie title from the user query, if present.
    Returns the title or None.
    """
    # Prefer quoted movie titles
    quoted = re.findall(r'"([^"]+)"|\'([^\']+)\'', user_text)
    if quoted:
        return quoted[0][0] or quoted[0][1]

    # Remove location part if present
    user_text_wo_location = re.sub(r"\bat\s+[A-Za-z0-9\s\-':]+$", "", user_text, flags=re.IGNORECASE).strip()

    # Patterns to extract movie title after trigger words
    patterns = [
        r"(?:showtimes\s+(?:for|of)|movie|screening of|watch|get|see|schedule of)\s+([A-Za-z0-9\s\-':]+)",
        r"^(?:show|find|see|watch|get)\s+([A-Za-z0-9\s\-':]+)",
    ]
    for p in patterns:
        m = re.search(p, user_text_wo_location, flags=re.IGNORECASE)
        if m:
            title = m.group(1).strip(" .!?")
            # Avoid extracting "all movies" as a movie title
            if title.lower() not in ["all movies", "movies"]:
                return title

    # If user says just "Barbie at AMC", extract before " at "
    m = re.match(r"([A-Za-z0-9\s\-':]+)\s+at\s+[A-Za-z0-9\s\-':]+$", user_text.strip(), flags=re.IGNORECASE)
    if m:
        title = m.group(1).strip(" .!?")
        if title.lower() not in ["all movies", "movies"]:
            return title

    # Fallback: If the user text is just a movie title
    if user_text.strip().lower() not in ["all movies", "movies"]:
        return user_text.strip(" .!?")
    return ""

def extract_location(user_text: str):
    """
    Extracts the location (theater) from the user query, if present.
    Returns the location or "".
    """
    # Prefer quoted locations
    quoted = re.findall(r'"([^"]+)"|\'([^\']+)\'', user_text)
    if quoted:
        return quoted[0][0] or quoted[0][1]

    # Look for "at <location>" at the end
    m = re.search(r"\bat\s+([A-Za-z0-9\s\-':]+)$", user_text, flags=re.IGNORECASE)
    if m:
        return m.group(1).strip(" .!?")
    
    patterns = [
        r"(?:showtimes\s+(?:for|of)|movie|screening of|watch|get|see|schedule of)\s+([A-Za-z0-9\s\-':]+)",
        r"^(?:show|find|see|watch|get)\s+([A-Za-z0-9\s\-':]+)",
    ]
    patterns = [
        r"(?:showtimes|screenings|show all movies|playing)\s+(?:at)\s+([A-Za-z0-9\s\-':]+)"
    ]
    for p in patterns:
        m = re.search(p, user_text, flags=re.IGNORECASE)
        if m:
            return m.group(1).strip(" .!?")

    return ""
def search_screening_event(user_query):
    """
    Enhanced search screening event handler:
    Properly handles all valid query cases:
    1. Location-only queries.
    2. Movie-only queries.
    3. Combined movie + location queries.
    Extracts and prints out the values from the 'showtimes' key in the JSON file.
    """
    serpapi_key = _get_serpapi_key()
    if not serpapi_key:
        return "SerpAPI key not set. Please add SERPAPI_KEY to .streamlit/secrets.toml or your environment variables."

    location = extract_location(user_query)
    movie_title = extract_movie_title(user_query)

    # Case 1: Location-only query
    if location and (not movie_title or movie_title.strip().lower() in ["showtimes", "", None]):
        search_query = f"showtimes at {location}"
        url = f"https://serpapi.com/search.json?q={search_query}&api_key={serpapi_key}"
        resp = requests.get(url)
        if resp.status_code != 200:
            return "Error contacting SerpAPI."

        data = resp.json()
        showtimes = data.get("showtimes", [])
        if not showtimes:
            google_url = f"https://www.google.com/search?q={urllib.parse.quote(search_query)}"
            return choose(
                [ # Giving varied responses with a 'moody tenager characteristic' for no results found
                    f"No movies found at **{location}**. Such is life 🤷 \n",
                    f"No movies found at **{location}**. Oh well 🤷 \n",
                    f"No movies found at **{location}**. Such is life 🤷 \n",
                    f"No movies found at **{location}**. We do not get what we want in life do we 🤷 \n",
                    f"No movies found at **{location}**. If only life was simpler 😤 \n"
                ]
            ) + '\n im lazy now so here are some links you can explore yourself \n ' + google_url 

        # Print out the raw 'showtimes' values from the JSON
        print("Raw 'showtimes' key from SerpAPI response:")
        print(showtimes)

        # Format the results
        result_lines = [f"Well, good for you dude. Here are the showtimes for movies at **{location}**:"]
        for day_entry in showtimes:
            day = f"{day_entry.get('day', 'Unknown day')} {day_entry.get('date', '')}"
            movies = day_entry.get("movies", [])
            for movie in movies:
                title = movie.get("name", "Unknown movie")
                times = []
                for showing in movie.get("showing", []):
                    times.extend(showing.get("time", []))
                # Add movie name and its times for the day
                if times:
                    times_str = ", ".join(times)
                    result_lines.append(f"- **{title}** ({day}): {times_str}")
        return "\n".join(result_lines)
    
    # Case 2: Movie-only query
    elif movie_title and not location:
        search_query = f"{movie_title} showtimes"
        url = f"https://serpapi.com/search.json?q={search_query}&api_key={serpapi_key}"
        resp = requests.get(url)
        if resp.status_code != 200:
            return "Error contacting SerpAPI."
        data = resp.json()
        showtimes = data.get("showtimes", [])

        if not showtimes: 
            google_url = f"https://www.google.com/search?q={urllib.parse.quote(search_query)}"
            return choose(
                [ # Giving varied responses with a 'moody tenager characteristic' for no results found
                    f"No showtimes found for **{movie_title}**. Such is life 🤷 \n",
                    f"No showtimes found for **{movie_title}**. Oh well 🤷 \n",
                    f"No showtimes found for **{movie_title}**. Such is life 🤷 \n",
                    f"No showtimes found for **{movie_title}**. We do not get what we want in life do we 🤷 \n",
                    f"No showtimes found for **{movie_title}**. If only life was simpler 😤 \n"
                ]
            ) + '\n im lazy now so here are some links you can explore yourself \n ' + google_url 
        
        result_lines = [f"Well, good for you dude. Here are the showtimes for **{movie_title}**:"]
        for day_entry in showtimes:
            day = day_entry.get("day", "Unknown day")
            theaters = day_entry.get("theaters", [])
            for theater in theaters:
                name = theater.get("name", "Unknown theater")
                address = theater.get("address", "")
                for showing in theater.get("showing", []):
                    times = ", ".join(showing.get("time", []))
                    result_lines.append(f"- {day} @ **{name}** ({address}): {times}")
        return "\n".join(result_lines)

    # Fallback Case: No sufficient data extracted from query
    return choose(
        [
            "Hey dude, Couldn't extract a valid movie title or location from your query. Try being more specific next time man.",
            "Look man, I couldn't figure out what you need—could you rephrase your query?"
        ]
    )