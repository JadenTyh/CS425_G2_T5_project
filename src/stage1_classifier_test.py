import torch
from transformers import DistilBertTokenizerFast, DistilBertForSequenceClassification

MODEL_DIR = "models/intent_classifier"

# Load trained model + tokenizer
tokenizer = DistilBertTokenizerFast.from_pretrained(MODEL_DIR)
model = DistilBertForSequenceClassification.from_pretrained(MODEL_DIR)

def classify(text):
    """Return the predicted intent for an input sentence."""
    inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True)
    logits = model(**inputs).logits
    pred_id = torch.argmax(logits, dim=1).item()
    return model.config.id2label[pred_id]

print("✅ Model Loaded!")
print("Type a message to classify it. Type 'exit' to quit.\n")

while True:
    user_input = input("You: ")
    
    if user_input.lower() in ["exit", "quit", "q"]:
        print("👋 Exiting test.")
        break
    
    prediction = classify(user_input)
    print(f"➡️ Intent: {prediction}\n")
