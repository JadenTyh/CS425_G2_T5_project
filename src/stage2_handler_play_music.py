import re
import subprocess
import random
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


# --- 3. NEW Recommendation Helpers ---

# Genre → Example playlists (YouTube)
GENRE_PLAYLISTS = {
    "lofi": ["lofi hip hop radio", "lofi beats to relax/study to"],
    "jazz": ["jazz for study", "smooth jazz playlist"],
    "r&b": ["r&b slow jams", "modern r&b mix"],
    "rock": ["90s rock playlist", "classic rock hits"],
    "indie": ["indie vibes playlist", "indie chill mix"],
    "pop": ["top pop hits", "today's top hits mix"],
}

# Mood → Playlist keywords
MOOD_KEYWORDS = {
    "sad": "sad songs playlist",
    "chill": "chill vibes playlist",
    "hype": "party bangers playlist",
    "study": "focus lofi beats",
    "sleep": "calm sleep music",
    "romantic": "love songs playlist",
    "gym": "workout pump mix",
}

# --- Artist Knowledge Base ---

GENRE_TO_ARTISTS = {
    # --- INDIE / BEDROOM POP / SOFT ALT ---
    "indie": [
        "Phoebe Bridgers","Mitski","The 1975","Beabadoobee","Men I Trust","Clairo","Dayglow","Snail Mail",
        "Lucy Dacus","Julien Baker","Boygenius","Japanese Breakfast","Soccer Mommy","Faye Webster",
        "Still Woozy","Wallows","Peach Pit","Rex Orange County","Hippo Campus","Mac DeMarco",
        "Arctic Monkeys","The Strokes","Cigarettes After Sex","Lana Del Rey","Weyes Blood","Sufjan Stevens",
        "Hozier","Moses Sumney","Bon Iver","Fleet Foxes"
    ],

    # --- LOFI / CHILLHOP / STUDY VIBES ---
    "lofi": [
        "Lofi Girl","Mondo Loops","potsu","Kudasai","Aso","eevee","Jinsang","Idealism","Nymano",
        "Oatmello","Aiguille","Sleepdealer","Kendall Miles","Leavv","SwuM","Burbank","In Love With a Ghost"
    ],

    # --- K-POP / ASIAN POP ---
    "k-pop": [
        "NewJeans","IVE","LE SSERAFIM","TWICE","SEVENTEEN","Stray Kids","ITZY","aespa","BLACKPINK",
        "BTS","Jungkook","Jimin","Big Bang","Red Velvet","Taeyeon","NCT DREAM","TXT","G-IDLE",
        "STAYC","LOONA","BOL4","AKMU","Kep1er"
    ],

    # --- POP (Modern / Mainstream) ---
    "pop": [
        "Taylor Swift","Olivia Rodrigo","Dua Lipa","Sabrina Carpenter","The Weeknd","Billie Eilish",
        "Ariana Grande","Ed Sheeran","SZA","Miley Cyrus","Lady Gaga","Selena Gomez","Lorde","Troye Sivan",
        "Sam Smith","Conan Gray","Reneé Rapp","RAYE","Tate McRae","Carly Rae Jepsen","Ellie Goulding",
        "Halsey","Khalid","Chappell Roan","Gracie Abrams"
    ],

    # --- ROCK / ALT ROCK / BAND VIBES ---
    "rock": [
        "Nirvana","Arctic Monkeys","Red Hot Chili Peppers","Queen","AC/DC","Radiohead","The Strokes",
        "The Killers","Green Day","Paramore","Foo Fighters","Pearl Jam","Soundgarden","The Smashing Pumpkins",
        "The Rolling Stones","Pink Floyd","Led Zeppelin","Blur","The Cure","The Smiths","Muse","My Chemical Romance"
    ],

    # --- R&B / SOUL / SMOOTH / MOODY ---
    "r&b": [
        "SZA","Brent Faiyaz","Daniel Caesar","The Weeknd","Frank Ocean","Khalid","Kehlani","Summer Walker",
        "Jhené Aiko","Giveon","Cleo Sol","Lucky Daye","Omar Apollo","Steve Lacy","Raveena","Joy Crookes"
    ],

    # --- HIP-HOP / ALTERNATIVE RAP / VIBEY RAP ---
    "hip-hop": [
        "Kendrick Lamar","J. Cole","Travis Scott","Tyler, The Creator","Baby Keem","A$AP Rocky","21 Savage",
        "Playboi Carti","Lil Uzi Vert","Joey Bada$$","JID","Denzel Curry","Earl Sweatshirt","Anderson .Paak",
        "Smino","Noname","Amine","Mac Miller","Cordae","Westside Boogie"
    ],

    # --- CITY POP / J-POP / VINTAGE ASIAN GROOVE ---
    "city pop": [
        "Miki Matsubara","Mariya Takeuchi","Anri","Tatsuro Yamashita","Taeko Ohnuki","Lamp","Fujii Kaze",
        "Vaundy","Aimer","Hikaru Utada","YOASOBI","King Gnu","Wednesday Campanella"
    ],

    # --- CHILL / ROMANTIC / LATE NIGHT (CROSS-GENRE) ---
    "chill": [
        "Joji","Laufey","Cigarettes After Sex","Daniel Caesar","Rex Orange County","Faye Webster",
        "Khalid","Raveena","Sufjan Stevens","Kacey Musgraves","Clairo","Men I Trust"
    ],

    # --- GYM / HYPE / ENERGY ---
    "hype": [
        "Travis Scott","21 Savage","Don Toliver","Drake","Central Cee","Lil Uzi Vert","Dua Lipa","Doja Cat",
        "Stray Kids","SEVENTEEN","BLACKPINK","The Weeknd","Skrillex","David Guetta"
    ]
}


# Quick Artist Similarity Map (expandable later)
SIMILAR_ARTISTS = {
    "SZA": ["Summer Walker", "Kehlani", "Jhené Aiko"],
    "Phoebe Bridgers": ["Lucy Dacus", "Julien Baker", "Boygenius"],
    "Laufey": ["Norah Jones", "Beabadoobee", "Faye Webster"],
    "Arctic Monkeys": ["The Strokes", "The 1975", "Wallows"],
    "Joji": ["Keshi", "DPR Ian", "Cigarettes After Sex"],
}

# Mood → Genre Mappings
MOOD_TO_GENRE = {
    "sad": "indie",
    "chill": "lofi",
    "study": "lofi",
    "hype": "rock",
    "romantic": "r&b",
    "gym": "rock",
}


def recommend_genre_playlist(user_text: str) -> str:
    """Ask user permission before playing a genre playlist."""
    for genre in GENRE_TO_ARTISTS:
        if genre.lower() in user_text.lower():
            return f"🎶 You mentioned **{genre}** music.\nShall I play some {genre} songs?"
    return "I can recommend music by genre — try saying: 'recommend some indie vibes'"


def recommend_artist_mix(user_text: str) -> str:
    """Recommend similar artists instead of searching."""
    for artist in SIMILAR_ARTISTS:
        if artist.lower() in user_text.lower():
            similar = SIMILAR_ARTISTS[artist]
            choices = ", ".join(similar)
            return f"If you like **{artist}**, you may also enjoy: **{choices}**.\nWant me to play some?"
    return "Tell me the artist again — I'll recommend similar artists."


def recommend_mood_playlist(user_text: str) -> str:
    """Recommend based on mood → genre → artist."""
    for mood in MOOD_TO_GENRE:
        if mood in user_text.lower():
            genre = MOOD_TO_GENRE[mood]
            artists = GENRE_TO_ARTISTS.get(genre, [])
            artist = artists[0] if artists else "some music"
            return f"🌙 For **{mood}** vibes, I recommend **{genre}**.\nShall I start with **{artist}**?"
    return "Tell me how you're feeling — sad, chill, hype, romantic, etc."

def play_from_genre(genre: str) -> str:
    """Pick a random artist and return a YouTube link."""
    import random
    artists = GENRE_TO_ARTISTS.get(genre, [])
    if not artists:
        return "I don't have enough artists in that genre yet."

    chosen = random.choice(artists)
    yt = youtube_search(f"{chosen} music")
    return f"🔥 Starting {genre} vibes with **{chosen}**:\n{yt}"


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
