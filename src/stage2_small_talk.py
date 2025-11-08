import torch
from transformers import GPT2LMHeadModel, GPT2Tokenizer
import os

# -----------------------------------------------------
# 1. Load the Fine-Tuned Small Talk Model
# -----------------------------------------------------

# Path to your small talk model directory
MODEL_PATH = os.path.join("models", "small_talk")

# Load tokenizer + model
tokenizer = GPT2Tokenizer.from_pretrained(MODEL_PATH)
model = GPT2LMHeadModel.from_pretrained(MODEL_PATH, device_map=None)

# Ensure padding token is set (GPT-2 does not have one by default)
tokenizer.pad_token = tokenizer.eos_token
model.config.pad_token_id = tokenizer.eos_token_id

# Move model to CPU (safe for Streamlit / local usage)
model = model.to("cpu")
model.eval()


# -----------------------------------------------------
# 2. Response Generation Function
# -----------------------------------------------------

def generate_response(user_message: str, max_length: int = 120) -> str:
    """
    Generates a small-talk conversational response using the fine-tuned GPT-2 model.
    """
    # Format like a conversation
    input_text = f"Human: {user_message}\nBot:"
    input_ids = tokenizer.encode(input_text, return_tensors="pt").to("cpu")

    # Generate the response
    with torch.no_grad():
        output = model.generate(
            input_ids,
            max_length=max_length,
            temperature=0.8,
            top_p=0.9,
            do_sample=True,
            repetition_penalty=1.2,
            no_repeat_ngram_size=3,
            pad_token_id=tokenizer.eos_token_id
        )

    # Decode + clean result
    response_text = tokenizer.decode(output[0], skip_special_tokens=True)

    # Extract only the part after "Bot:"
    if "Bot:" in response_text:
        response_text = response_text.split("Bot:")[-1].strip()

    return response_text
