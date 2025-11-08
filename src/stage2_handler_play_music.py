import re
import subprocess
import random
import streamlit as st
from stage2_music_knowledge import GENRE_TO_ARTISTS, SIMILAR_ARTISTS, MOOD_TO_GENRE

from typing import Optional

# --- 1. Regex for direct music links ---
SPOTIFY_RE = re.compile(
    r"https?://open\.spotify\.com/(track|album|playlist|episode)/[A-Za-z0-9]+(?:\?[^\s]+)?",
    re.IGNORECASE
)

YOUTUBE_RE = re.compile(
    r"https?://(?:www\.)?(?:youtube\.com/watch\?v=[A-Za-z0-9_\-]+|youtu\.be/[A-Za-z0-9_\-]+)",
    re.IGNORECASE
)


# --- 2. Core Extraction Helpers ---
def extract_spotify_link(text: str) -> Optional[str]:
    match = SPOTIFY_RE.search(text)
    return match.group(0) if match else None


def extract_youtube_link(text: str) -> Optional[str]:
    match = YOUTUBE_RE.search(text)
    return match.group(0) if match else None


def youtube_search(query: str) -> Optional[str]:
    """Search YouTube and return the top video result URL."""
    try:
        video_id = subprocess.check_output(
            ["yt-dlp", f"ytsearch1:{query}", "--get-id"],
            stderr=subprocess.DEVNULL
        ).decode().strip()
        return f"https://www.youtube.com/watch?v={video_id}"
    except Exception:
        return None


# --- 3. Recommendation Helpers ---



import re

def extract_artist_name(text):
    """
    Attempts to detect an artist name in user input by fuzzy scanning.
    Returns the matched artist string or None.
    """
    text_lower = text.lower()

    for group in GENRE_TO_ARTISTS.values():
        for artist in group:
            if artist.lower() in text_lower:
                return artist
    
    # fallback: uppercase words that look like names
    candidates = re.findall(r"[A-Z][a-z]+(?:\s[A-Z][a-z]+)*", text)
    return candidates[0] if candidates else None

def find_similar_artists(artist):
    """
    Returns similar artists. Handles None safely.
    """
    # No artist detected
    if not artist:
        return ["Laufey", "Phoebe Bridgers", "The 1975"]   # safe fallback recs

    artist_lower = artist.lower()

    for group_name, artist_list in GENRE_TO_ARTISTS.items():
        for a in artist_list:
            if a.lower() == artist_lower:
                recs = [x for x in artist_list if x.lower() != artist_lower]
                return recs[:3]

    # fallback if artist exists but not in our groups
    return ["Laufey", "Men I Trust", "Clairo"]



def recommend_genre_playlist(user_text: str) -> str:
    """Ask user permission before playing a genre playlist."""
    for genre in GENRE_TO_ARTISTS:
        if genre.lower() in user_text.lower():
            st.session_state.last_music_action = {
                "pending": True,
                "action": "recommend_genre",
                "genre": genre,
            }
            return f"🎶 You mentioned **{genre}** music.\nShall I play some {genre} songs?"

    return "I can recommend music by genre — try saying: 'recommend some indie vibes'"


def recommend_artist_mix(user_text):
    artist = extract_artist_name(user_text)
    suggestions = find_similar_artists(artist)

    # Determine genre for future playback
    genre = None
    for g, artists in GENRE_TO_ARTISTS.items():
        if artist in artists:
            genre = g
            break

    st.session_state.last_music_action = {
        "action": "recommend_artist",
        "artist": artist,
        "suggested": suggestions,
        "genre": genre  # store genre for follow-up
    }

    return f"If you like **{artist}**, you may also enjoy: {', '.join(suggestions)}.\nWant me to play one?"

def recommend_mood_playlist(user_text):
    for mood in MOOD_TO_GENRE:
        if mood in user_text.lower():
            genre = MOOD_TO_GENRE[mood]

            st.session_state.last_music_action = {
                "action": "play_mood",
                "genre": genre
            }

            artists = GENRE_TO_ARTISTS.get(genre, [])
            sample = artists[0] if artists else "something good"
            return f"🌙 For **{mood}** vibes, I recommend **{genre}**.\nShall I start with **{sample}**?"

    return "Tell me how you're feeling — sad, chill, hype, romantic, etc."


def play_from_genre(genre: str) -> str:
    """Pick a random artist and return an embedded YouTube link."""
    import random

    artists = GENRE_TO_ARTISTS.get(genre, [])
    if not artists:
        return "I don't have enough artists in that genre yet."

    chosen = random.choice(artists)
    yt = youtube_search(f"{chosen} music")

    # Return separate text and link (embedding handled by UI)
    if yt:
        return f"🔥 Starting {genre} vibes with **{chosen}**!\n{yt}"
    else:
        return f"Couldn't find a track for {chosen} right now."



# --- 4. Main Music Intent Handler ---

def handle_music_request(user_text: str, sub_intent: str = "play_track") -> str:
    
    # Direct links
    if extract_spotify_link(user_text):
        return f"Playing on Spotify:\n{extract_spotify_link(user_text)}"

    if extract_youtube_link(user_text):
        return f"Playing via YouTube:\n{extract_youtube_link(user_text)}"

    # Sub-intent routing
    if sub_intent == "recommend_genre":
        return recommend_genre_playlist(user_text)

    if sub_intent == "recommend_artist":
        return recommend_artist_mix(user_text)

    if sub_intent == "play_mood":
        return recommend_mood_playlist(user_text)

    # Default: treat text as a track search
    result = youtube_search(user_text)
    if result:
        return f"Found on YouTube:\n{result}"

    return "Hmm, I couldn't find that track — try giving me an artist or a lyric."
