import streamlit as st
import torch
from transformers import DistilBertTokenizerFast, DistilBertForSequenceClassification

# Import small talk
from stage2_small_talk import generate_response

# Import our Stage 2 models
from stage2_handler_play_music import (
    handle_music_request,
    recommend_genre_playlist,
    recommend_artist_mix,
    recommend_mood_playlist,
    play_from_genre,
    GENRE_TO_ARTISTS
)
from stage2_predict_music import classify_music_request
from stage2_handler_weather import handle_weather_request


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
st.write("Ask me to play music, get the weather, or just chat with me!")


# --- 3. Chat Input ---

user_input = st.text_input(
    "You:", placeholder="Example: play some jazz / add this to my playlist / hello"
)


# --- 4. Chat Logic ---

if user_input:
    
    if "yes" in user_input.lower() and st.session_state.get("pending_genre"):
        genre = st.session_state["pending_genre"]
        st.session_state["pending_genre"] = None
        reply = play_from_genre(genre)
        st.write(reply)
        st.stop()


    # a) Determine user intent using classifier (Stage 1)
    intent = classify_intent(user_input)

    # b) If user wants music → call Stage 2 handler
    if intent == "play_music":
        if intent == "play_music":
            sub = classify_music_request(user_input)
            print(f"[DEBUG] Sub-intent detected: {sub}")
            if sub == "play_track":
                reply = handle_music_request(user_input, sub)

            elif sub == "recommend_genre":
                # will return a YouTube/Spotify list
                reply = recommend_genre_playlist(user_input)
                if "Shall I play" in reply:
                    for genre in GENRE_TO_ARTISTS.keys():
                        if genre in user_input.lower():
                            st.session_state["pending_genre"] = genre


            elif sub == "recommend_artist":
                reply = recommend_artist_mix(user_input)

            elif sub == "play_mood":
                reply = recommend_mood_playlist(user_input)

            else:
                reply = handle_music_request(user_input)  # safe fallback

    elif intent == "weather_query":
        reply = handle_weather_request(user_input)

    # c) Otherwise it's small talk → return small talk reply
    else:
        reply = generate_response(user_input)

    # d) Display response
    # --- Display response with embedded media if possible ---
    if "youtube.com" in reply or "youtu.be" in reply:
        import re

        yt_link = re.search(r"https?://\S+", reply).group(0)
        st.video(yt_link)

    elif reply.startswith("spotify_player::"):
        spotify_link = reply.replace("spotify_player::", "")
        st.markdown(
            f"""
            <iframe src="https://open.spotify.com/embed/track/{spotify_link.split('/')[-1]}" 
            width="100%" height="152" frameborder="0" allowtransparency="true" allow="encrypted-media"></iframe>
        """,
            unsafe_allow_html=True,
        )

    else:
        st.write(reply)
