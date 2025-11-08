import streamlit as st
import torch
from transformers import DistilBertTokenizerFast, DistilBertForSequenceClassification

# Import small talk
from stage1_1_small_talk import generate_response

# Import our Stage 2 action handler (YouTube + Spotify behavior)
from stage2_handler_play_music import handle_music_request
from stage2_handler_weather import handle_weather_request


# --- 1. Load Trained Intent Classifier Model ---

MODEL_DIR = "models/intent_classifier"  # Folder where stage1_classifier saved the model

# Load the tokenizer and fine-tuned model from disk
tokenizer = DistilBertTokenizerFast.from_pretrained(MODEL_DIR)
model = DistilBertForSequenceClassification.from_pretrained(
    MODEL_DIR,
    device_map=None,       # prevent Accelerate from placing model on 'meta'
)
model.to("cpu") 

def classify_intent(text):
    """
    Uses the trained DistilBERT classifier to return the predicted intent label.
    """
    inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True)
    logits = model(**inputs).logits                      # Model forward pass → output logits
    pred_id = torch.argmax(logits, dim=1).item()         # Pick highest probability class
    return model.config.id2label[pred_id]                # Convert ID back to readable label


# --- 2. Streamlit UI Setup ---

st.set_page_config(page_title="Music & Weather Chatbot", page_icon="🎵")
st.title("🎵 Music & Weather Chatbot")
st.write("Ask me to play music, get the weather, or just chat with me!")


# --- 3. Chat Input ---

user_input = st.text_input("You:", placeholder="Example: play some jazz / add this to my playlist / hello")


# --- 4. Chat Logic ---

if user_input:

    # Step 1: Determine user intent using classifier (Stage 1)
    intent = classify_intent(user_input)

    # Step 2: If user wants music → call Stage 2 handler
    if intent == "play_music":
        reply = handle_music_request(user_input)
    elif intent == "weather_query":
        reply = handle_weather_request(user_input)

    # Step 3: Otherwise it's small talk → return small talk reply
    else:
        reply = generate_response(user_input)

    # Step 4: Display response
    # --- Display response with embedded media if possible ---
    if "youtube.com" in reply or "youtu.be" in reply:
        import re
        yt_link = re.search(r'https?://\S+', reply).group(0)
        st.video(yt_link)

    elif reply.startswith("spotify_player::"):
        spotify_link = reply.replace("spotify_player::", "")
        st.markdown(f"""
            <iframe src="https://open.spotify.com/embed/track/{spotify_link.split('/')[-1]}" 
            width="100%" height="152" frameborder="0" allowtransparency="true" allow="encrypted-media"></iframe>
        """, unsafe_allow_html=True)

    else:
        st.write(reply)