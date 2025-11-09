import re
import subprocess
import random
import streamlit as st
from stage2_music_knowledge import GENRE_TO_ARTISTS, SIMILAR_ARTISTS, MOOD_TO_GENRE
from random import choice as choose
from typing import Optional

# --- 1. Regex for direct music links ---
SPOTIFY_RE = re.compile(
    r"https?://open\.spotify\.com/(track|album|playlist|episode)/[A-Za-z0-9]+(?:\?[^\s]+)?",
    re.IGNORECASE,
)

YOUTUBE_RE = re.compile(
    r"https?://(?:www\.)?(?:youtube\.com/watch\?v=[A-Za-z0-9_\-]+|youtu\.be/[A-Za-z0-9_\-]+)",
    re.IGNORECASE,
)


# --- 2. Core Extraction Helpers ---
def extract_spotify_link(text: str) -> Optional[str]:
    match = SPOTIFY_RE.search(text)
    return match.group(0) if match else None


def extract_youtube_link(text: str) -> Optional[str]:
    match = YOUTUBE_RE.search(text)
    return match.group(0) if match else None


def youtube_search(query: str) -> Optional[str]:
    """
    Searches specifically for real music tracks (YouTube Music auto-generated Topic tracks).
    Avoids interviews, shorts, random edits, etc.
    """
    try:
        # 1) Clean query to avoid accidental non-music matches
        clean_query = re.sub(
            r"(official video|live|interview|making of|behind the scenes)",
            "",
            query,
            flags=re.I,
        ).strip()

        # 2) Force YouTube Music 'Topic' channel search
        topic_query = f"ytsearch1:{clean_query} - Topic"

        video_id = (
            subprocess.check_output(
                [
                    "yt-dlp",
                    topic_query,
                    "--get-id",
                    "--default-search",
                    "ytsearch",
                    "--match-filter",
                    "duration < 600",  # avoid long videos
                ],
                stderr=subprocess.DEVNULL,
            )
            .decode()
            .strip()
        )

        return f"https://www.youtube.com/watch?v={video_id}"

    except Exception:
        # fallback to normal search with "lyrics" bias (still real music)
        try:
            video_id = (
                subprocess.check_output(
                    [
                        "yt-dlp",
                        f"ytsearch1:{query} lyrics",
                        "--get-id",
                    ],
                    stderr=subprocess.DEVNULL,
                )
                .decode()
                .strip()
            )
            return f"https://www.youtube.com/watch?v={video_id}"
        except:
            return None


# --- 3. Recommendation Helpers ---


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


import random


def find_similar_artists(artist: str):
    if not artist:
        return random.sample(GENRE_TO_ARTISTS["indie"], 3)

    # Normalize
    artist_lower = artist.lower()

    # Randomize direct similarity list
    if artist_lower in {a.lower(): a for a in SIMILAR_ARTISTS}.keys():
        # Get the exact key in correct case
        real_key = next(a for a in SIMILAR_ARTISTS if a.lower() == artist_lower)
        sims = SIMILAR_ARTISTS[real_key]
        return random.sample(sims, min(len(sims), 3))

    # Genre-based fallback
    for genre, artist_list in GENRE_TO_ARTISTS.items():
        if any(a.lower() == artist_lower for a in artist_list):
            others = [a for a in artist_list if a.lower() != artist_lower]
            return random.sample(others, min(len(others), 3))

    # Final fallback
    return None


def recommend_genre_playlist(user_text: str) -> str:
    """Ask user permission before playing a genre playlist."""
    for genre in GENRE_TO_ARTISTS:
        if genre.lower() in user_text.lower():
            st.session_state.last_music_action = {
                "pending": True,
                "action": "recommend_genre",
                "genre": genre,
            }
            return choose(
                [
                    f"So you want **{genre}** vibes. Cool, I guess.\nWant me to play some?",
                    f"Alright, **{genre}**. I can put something on… if you *insist*.\nSay yes or whatever.",
                    f"**{genre}** huh. Should I start something or are we just thinking about it?",
                    f"yeah sure, **{genre}**. I can play a playlist.\nDo you want that or nah?",
                    f"if you want **{genre}** stuff, I can queue it.\nJust say 'yes' I guess.",
                    f"Okay. **{genre}** music. Should I actually play some?",
                    f"mm. **{genre}**. I can start something… but only if you really want.",
                ]
            )

    return choose(
        [
            "You can tell me a genre, you know.",
            "idk what genre you're talking about. try again.",
            "huh? just say 'indie', 'lofi', 'pop' or something.",
            "I can't read your mind dude, say a real genre.",
            "just… say the genre. please.",
        ]
    )


def recommend_artist_mix(user_text):
    artist = extract_artist_name(user_text)
    suggestions = find_similar_artists(artist)

    # If we couldn't find that artist anywhere in our DB:
    if suggestions is None:
        return random.choice(
            [
                f"Uh... yeah I don't really know **{artist}** like that. My bad.",
                f"Never heard of **{artist}**. Maybe I'm just uncultured or whatever.",
                f"Yeah nah, **{artist}** isn't in my brain. Try someone else maybe?",
                f"I'd love to pretend I know **{artist}**, but I don't. Sorry or something.",
                f"Bro I swear I don't have **{artist}** in my system. Give me a different name.",
            ]
        )

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
        "genre": genre,  # store genre for follow-up
    }

    return choose(
        [
            f"So you listen to **{artist}**, huh. Try {', '.join(suggestions)} or whatever.\nWanna play one?",
            f"Alright, if you're into **{artist}**, people also go for {', '.join(suggestions)}.\nShould I play something or nah?",
            f"Cool taste, I guess. {', '.join(suggestions)} are kinda the same vibe.\nWant me to start some music?",
            f"Yeah okay, **{artist}** fans usually listen to {', '.join(suggestions)}.\nI can play one… if you *really* want.",
            f"mm. **{artist}**. fine. try {', '.join(suggestions)}.\nShould I actually play one or are we just talking?",
            f"I mean, sure. {', '.join(suggestions)} are similar.\nSay 'yes' if you want me to hit play.",
            f"Right. If you like **{artist}**, then {', '.join(suggestions)} makes sense.\nWant me to cue one up?",
        ]
    )


def recommend_mood_playlist(user_text):
    for mood in MOOD_TO_GENRE:
        if mood in user_text.lower():
            genre = MOOD_TO_GENRE[mood]

            artists = GENRE_TO_ARTISTS.get(genre, [])
            sample = random.choice(artists) if artists else None

            st.session_state.last_music_action = {
                "action": "play_mood",
                "genre": genre,
                "artist": sample,
            }

            if sample:
                return choose(
                    [
                        f"so you're feeling **{mood}**... fine. **{genre}** kinda fits.\nWant me to play **{sample}** or whatever?",
                        f"**{mood}** mood huh. guess **{genre}** works.\nshould i start **{sample}** or nah?",
                        f"okay. **{genre}** for **{mood}** vibes.\nwant me to play **{sample}**?",
                        f"yeah yeah, **{mood}**. i'll pick **{genre}**.\n**{sample}** first? say 'yes' if you care.",
                        f"alright bro. **{mood}** = **{genre}**.\nyou want **{sample}** or should i pretend you didn't say anything?",
                        f"fine. i'll go **{genre}**. **{sample}** is right there.\nwant it or no?",
                        f"cool mood i guess. starting with **{sample}**... but only if you actually want it. say yes.",
                    ]
                )
            else:
                return choose(
                    [
                        f"**{mood}** vibes means **{genre}**, normally.\nwant me to just pick something?",
                        f"idk man, **{genre}** works for **{mood}**.\nshould i choose a track or what?",
                        f"**{mood}** mood detected. **{genre}** time.\nyou want me to pick something? yes/no.",
                        f"i can start something in **{genre}** if you want.\njust say yes i guess.",
                        f"alright bro. **{genre}** fits.\nwanna let me choose the first song or nah?",
                    ]
                )

    #  No mood found → ask the user *and store that the bot expects a mood*
    st.session_state.last_music_action = {
        "action": "ask_mood"  # <--- new follow-up state
    }
    return choose(
        [
            "ok but like… how are you even feeling rn. (sad / chill / hype / romantic / gym / study)",
            "idk just tell me your vibe. sad? chill? hype? romantic? gym? study? pick one.",
            "sure whatever. what's the mood then. sad, chill, hype, romantic, gym, study?",
            "fine. what’s the *vibe*? sad / chill / hype / romantic / gym / study. pick one so I can do stuff.",
            "lol okay but what's your emotional damage level. sad / chill / hype / romantic / gym / study?",
            "i can’t read minds. just say sad, chill, hype, romantic, gym or study.",
            "cool, mood check time. which one are you: sad, chill, hype, romantic, gym, or study?",
        ]
    )


def play_from_genre(genre: str) -> str:
    """Pick a random artist and return an embedded YouTube link (teenager edition)."""
    import random

    artists = GENRE_TO_ARTISTS.get(genre, [])
    if not artists:
        return choose(
            [
                "idk dude, I barely even know that genre.",
                "no clue who even makes music in that genre.",
                "bro that genre is like... empty in my brain.",
                "can't play something that doesn't exist lol",
                "ask me for literally any other genre.",
            ]
        )

    chosen = random.choice(artists)
    yt = youtube_search(f"{chosen} music")

    if yt:
        return choose(
            [
                f"fine. **{chosen}** is kinda {genre} or whatever.\n{yt}",
                f"okay starting some **{genre}** stuff.\n**{chosen}**. don't say I never do anything.\n{yt}",
                f"here. **{chosen}**. it's **{genre}** vibes.\njust listen I guess.\n{yt}",
                f"starting **{genre}** with **{chosen}**.\ntry not to skip it instantly.\n{yt}",
                f"cool. **{chosen}** in **{genre}** lane.\npress play or don't idc.\n{yt}",
            ]
        )
    else:
        return choose(
            [
                f"couldn’t find anything for **{chosen}**. shocking.",
                f"youtube is being weird. **{chosen}** is hiding.",
                f"bruh. the universe said no to **{chosen}** today.",
                f"yeah so... no track for **{chosen}** right now. unlucky.",
                f"my bad. music void. try again or something.",
            ]
        )


# --- 4. Main Music Intent Handler ---


def handle_music_request(user_text: str, sub_intent: str = "play_track") -> str:

    # Direct links
    spotify = extract_spotify_link(user_text)
    if spotify:
        return choose(
            [
                f"cool. spotify link. playing it or whatever:\n{spotify}",
                f"yeah yeah spotify. here:\n{spotify}",
                f"fine. opening spotify. happy now?\n{spotify}",
                f"if you insist on spotify:\n{spotify}",
                f"here. spotify. I literally do not care:\n{spotify}",
            ]
        )

    youtube = extract_youtube_link(user_text)
    if youtube:
        return choose(
            [
                f"youtube link detected. pressing play:\n{youtube}",
                f"oh wow a youtube link. crazy. here:\n{youtube}",
                f"fine. youtube time:\n{youtube}",
                f"okay sure, youtube:\n{youtube}",
                f"here's your youtube thing:\n{youtube}",
            ]
        )

    # Sub-intent routing
    if sub_intent == "recommend_genre":
        return recommend_genre_playlist(user_text)

    if sub_intent == "recommend_artist":
        return recommend_artist_mix(user_text)

    if sub_intent == "play_mood":
        return recommend_mood_playlist(user_text)

    # Default: treat input as a track search
    result = youtube_search(user_text)
    if result:
        return choose(
            [
                f"found something on youtube I guess:\n{result}",
                f"here, this came up first. don't blame me:\n{result}",
                f"alright. this is probably what you meant:\n{result}",
                f"okay okay chill. playing this:\n{result}",
                f"here. music. enjoy or whatever:\n{result}",
            ]
        )

    return choose(
        [
            "bro I cannot find that. say it like a normal person.",
            "nothing came up. tragic.",
            "idk what song that is. try again but like… clearer.",
            "search results: zero. vibe: dead.",
            "nope. I got nothing. rephrase maybe?",
        ]
    )
