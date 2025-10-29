import re
from typing import Optional

# Precompile regexes for common music link providers
SPOTIFY_RE = re.compile(r"https?://open\.spotify\.com/(track|album|playlist|episode)/[A-Za-z0-9]+(?:\?[^\s]+)?", re.IGNORECASE)
YOUTUBE_RE = re.compile(r"https?://(?:www\.)?(?:youtube\.com/watch\?v=[A-Za-z0-9_\-]+|youtu\.be/[A-Za-z0-9_\-]+)(?:\?[^\s]+)?", re.IGNORECASE)
SOUNDCLOUD_RE = re.compile(r"https?://soundcloud\.com/[^\s]+", re.IGNORECASE)

PROVIDER_PATTERNS = [SPOTIFY_RE, YOUTUBE_RE, SOUNDCLOUD_RE]

def extract_music_link(text: str) -> Optional[str]:
    """Return the first detected music link in text, or None if not found."""
    if not text:
        return None
    for pat in PROVIDER_PATTERNS:
        m = pat.search(text)
        if m:
            return m.group(0)
    return None

def build_confirmation(link: str) -> str:
    """Return a user-facing confirmation message for the music action."""
    return f"Got it — playing your music link: {link}"