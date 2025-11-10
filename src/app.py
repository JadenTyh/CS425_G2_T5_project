import streamlit as st
import torch
import re
import random
from transformers import DistilBertTokenizerFast, DistilBertForSequenceClassification

# Import our Stage 2 models
from stage2_small_talk import generate_response
from stage2_handler_play_music import (
    handle_music_request,
    recommend_genre_playlist,
    recommend_artist_mix,
    recommend_mood_playlist,
    play_from_genre,
    GENRE_TO_ARTISTS,
)
from stage2_predict_music import classify_music_request
from stage2_handler_weather import handle_weather_request
from stage2_confirm import is_yes, is_no

if "last_music_action" not in st.session_state:
    st.session_state.last_music_action = None


# helper function to randomize text response
def choose(*options):
    return random.choice(options)


# helper function to display response
def show_reply(reply):
    """Embed YouTube/Spotify links if present, else print text."""

    # YouTube embed
    yt_match = re.search(r"(https?://\S+)", reply)
    if yt_match and (
        "youtube.com" in yt_match.group(1) or "youtu.be" in yt_match.group(1)
    ):
        yt_link = yt_match.group(1)
        text = reply.replace(yt_link, "").strip()
        if text:
            st.markdown(text)
        st.video(yt_link)
        return

    # Spotify embed
    if reply.startswith("spotify_player::"):
        spotify_link = reply.replace("spotify_player::", "")
        st.markdown(
            f"""
            <iframe src="https://open.spotify.com/embed/track/{spotify_link.split('/')[-1]}"
            width="100%" height="152" frameborder="0" allowtransparency="true" allow="encrypted-media"></iframe>
            """,
            unsafe_allow_html=True,
        )
        return

    # Default case
    st.write(reply)


# --- 1. Load Trained Intent Classifier Model ---

MODEL_DIR = "models/intent_classifier"  # Folder where stage1_classifier saved the model

# Load the tokenizer and fine-tuned model from disk
tokenizer = DistilBertTokenizerFast.from_pretrained(MODEL_DIR)
model = DistilBertForSequenceClassification.from_pretrained(
    MODEL_DIR,
    device_map=None,  # prevent Accelerate from placing model on 'meta'
)
model.to("cpu")


def classify_intent(text):
    """
    Uses the trained DistilBERT classifier to return the predicted intent label.
    """
    inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True)
    logits = model(**inputs).logits  # Model forward pass → output logits
    pred_id = torch.argmax(logits, dim=1).item()  # Pick highest probability class
    return model.config.id2label[pred_id]  # Convert ID back to readable label


# --- 2. Streamlit UI Setup ---

st.set_page_config(page_title="Music & Weather Chatbot", page_icon="🎵")
st.title("🎵 Music & Weather Chatbot")
show_reply(
    choose(
        "Yeah, I'm here. Ask for music, weather, whatever.",
        "What do you want? Music? Weather? Small talk? Cool.",
        "I'm awake. Barely. What do you need.",
        "Sure. I can play music or whatever. Just say it.",
    )
)


# --- 3. Chat Input ---

# --- Reset text input BEFORE drawing widget ---
if "chat_buffer" not in st.session_state:
    st.session_state.chat_buffer = ""  # stores last submitted message temporarily


def store_and_clear():
    st.session_state.chat_buffer = st.session_state.chat_input  # save message
    st.session_state.chat_input = ""  # clear box immediately


user_input = st.text_input(
    "You:",
    placeholder="Example: what is the weather / hello there / play some songs / artists like joji",
    key="chat_input",
    on_change=store_and_clear,  # store then clear
)

# --- 4. Chat Logic ---


def run_chat():
    user_text = st.session_state.chat_buffer.strip()
    if not user_text:
        return

    # RESET buffer after we capture it
    st.session_state.chat_buffer = ""

    # --- Conversation Follow-up Handling (Yes/No to music suggestions) ---
    # --- FOLLOW-UP STATE CHECK ---
    if st.session_state.last_music_action:
        last = st.session_state.last_music_action
        # for asking mood
        if last["action"] == "ask_mood":
            # If user responds with a mood, re-run mood recommend on it
            mood_guess = recommend_mood_playlist(user_text)
            show_reply(mood_guess)
            return

        # YES
        if is_yes(user_text):
            # clear context for small talk
            st.session_state.last_music_action = None
            # If mood recommendation follow-up
            if last["action"] == "play_mood":
                artist = last.get("artist")
                genre = last.get("genre")

                if artist:
                    yt = handle_music_request(artist, sub_intent="play_track")
                    st.markdown(
                        choose(
                            f"Playing **{artist}**. I guess.",
                            f"Okay. **{artist}**. Sure.",
                            f"Fine. Here's **{artist}**.",
                            f"Alright, **{artist}**. Don't say I never do anything.",
                            f"Cool. **{artist}** is on. Chill or whatever.",
                        )
                    )
                    show_reply(yt)
                else:
                    # fallback: play random from genre
                    reply = play_from_genre(genre)
                    show_reply(reply)

                st.session_state.last_music_action = None
                return

            # If artist recommendation follow-up
            if last["action"] == "recommend_artist":
                artist = (
                    last.get("artist") or last["suggested"][0]
                )  # name user asked about
                suggestions = last.get("suggested", [])

                # pick something to play
                artist_to_play = suggestions[0] if suggestions else artist
                yt = handle_music_request(artist_to_play, sub_intent="play_track")

                st.markdown(
                    choose(
                        f"If you're into **{artist}**, maybe try {', '.join(suggestions)}. Want one or not?",
                        f"Okay so **{artist}**. People also listen to {', '.join(suggestions)}. Should I play something?",
                        f"Whatever, here's some similar artists: {', '.join(suggestions)}. Want me to start?",
                        f"Cool taste. {', '.join(suggestions)} are kinda close. Play?",
                        f"Fine. Try {', '.join(suggestions)} I guess. Should I play one?",
                    )
                )
                show_reply(yt)
                return

            # If genre recommendation follow-up
            elif last["action"] == "recommend_genre":
                genre = last["genre"]
                reply = play_from_genre(genre)
                show_reply(reply)
                return

        # NO
        elif is_no(user_text):
            st.session_state.last_music_action = None
            show_reply(
                choose(
                    "Okay then.",
                    "Cool. No problem.",
                    "Sure. Whatever you want.",
                    "Alright, don't worry about it.",
                    "Yeah that's fine.",
                )
            )

            return

    # a) Determine user intent using classifier (Stage 1)
    intent = classify_intent(user_text)
    print(f"[DEBUG] Main-intent detected: {intent}")
    # b) If user wants music → call Stage 2 handler
    if intent == "play_music":
        sub = classify_music_request(user_text)
        print(f"[DEBUG] Sub-intent detected: {sub}")
        if sub == "play_track":
            reply = handle_music_request(user_text, sub)

        elif sub == "recommend_genre":
            # will return a YouTube/Spotify list
            reply = recommend_genre_playlist(user_text)
            if "Shall I play" in reply:
                for genre in GENRE_TO_ARTISTS.keys():
                    if genre in user_text.lower():
                        st.session_state["pending_genre"] = genre

        elif sub == "recommend_artist":
            reply = recommend_artist_mix(user_text)

        elif sub == "play_mood":
            reply = recommend_mood_playlist(user_text)

        else:
            reply = handle_music_request(user_text)  # safe fallback

    # c) or it's weather
    elif intent == "weather_query":
        reply = handle_weather_request(user_text)

    # d) Otherwise it's small talk → return small talk reply
    else:
        reply = generate_response(user_text)

    # e) Display response
    # --- Display response with embedded media if possible ---
    show_reply(reply)
    return


run_chat()
