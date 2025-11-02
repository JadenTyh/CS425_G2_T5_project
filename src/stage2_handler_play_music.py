import re
import subprocess
from typing import Optional

# --- 1. Precompiled Regex for Music Links ---

SPOTIFY_RE = re.compile(
    r"https?://open\.spotify\.com/(track|album|playlist|episode)/[A-Za-z0-9]+(?:\?[^\s]+)?",
    re.IGNORECASE
)

YOUTUBE_RE = re.compile(
    r"https?://(?:www\.)?(?:youtube\.com/watch\?v=[A-Za-z0-9_\-]+|youtu\.be/[A-Za-z0-9_\-]+)",
    re.IGNORECASE
)

# --- 2. Core Extraction Functions ---

def extract_spotify_link(text: str) -> Optional[str]:
    """Returns Spotify link if present, else None."""
    match = SPOTIFY_RE.search(text)
    return match.group(0) if match else None


def extract_youtube_link(text: str) -> Optional[str]:
    """Returns YouTube link if present, else None."""
    match = YOUTUBE_RE.search(text)
    return match.group(0) if match else None


def youtube_search(query: str) -> Optional[str]:
    """
    Takes a string (song name, playlist name, etc.)
    Returns a top YouTube music search result URL.
    """
    try:
        video_id = subprocess.check_output(
            ["yt-dlp", f"ytsearch1:{query}", "--get-id"],
            stderr=subprocess.DEVNULL
        ).decode().strip()
        return f"https://www.youtube.com/watch?v={video_id}"
    except Exception:
        return None

# --- 3. Response Logic ---

def handle_music_request(user_text: str) -> str:
    """Determines how to respond to a play_music intent."""
    
    # Case 1: Spotify link directly present → return it
    spotify = extract_spotify_link(user_text)
    if spotify:
        return f"🎧 Playing on Spotify:\n{spotify}"

    # Case 2: YouTube link already provided → return it
    youtube = extract_youtube_link(user_text)
    if youtube:
        return f"🎬 Playing via YouTube:\n{youtube}"

    # Case 3: Need to search YouTube
    yt_result = youtube_search(user_text)
    if yt_result:
        return f"🔍 Found on YouTube:\n{yt_result}"

    # Case 4: Nothing matched
    return "Hmm, I couldn't find that song — try being more specific."
