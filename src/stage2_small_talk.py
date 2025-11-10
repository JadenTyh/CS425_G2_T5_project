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

def generate_response(prompt, max_length=100):
    model.eval()
    input_text = f"Human: {prompt}\nBot:"
    input_ids = tokenizer.encode(input_text, return_tensors='pt').to(model.device)

    with torch.no_grad():
        output = model.generate(
            input_ids,
            max_length=max_length,
            num_return_sequences=1,
            temperature=0.8,
            top_p=0.9,
            do_sample=True,
            pad_token_id=tokenizer.eos_token_id,
            repetition_penalty=1.2,
            no_repeat_ngram_size=3
        )

    response = tokenizer.decode(output[0], skip_special_tokens=True)
    bot_response = response.split('Bot:')[-1].strip()

    # Split into sentences
    import re
    sentences = re.split(r'([.!?])', bot_response)

    # Reconstruct complete sentences (text + punctuation)
    complete_sentences = []
    for i in range(0, len(sentences)-1, 2):
        if i+1 < len(sentences) and sentences[i].strip():
            complete_sentences.append(sentences[i] + sentences[i+1])

    # Keep only first 2 sentences
    if len(complete_sentences) >= 2:
        result = ''.join(complete_sentences[:2]).strip()
    elif len(complete_sentences) == 1:
        result = complete_sentences[0].strip()
    else:
        # If no complete sentence, add period
        result = bot_response + '.' if bot_response else "I'm not sure how to respond."

    return result
