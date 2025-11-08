import torch
from transformers import DistilBertTokenizerFast, DistilBertForSequenceClassification

MODEL_DIR = "models/music_subintent_classifier"

tokenizer = DistilBertTokenizerFast.from_pretrained(MODEL_DIR)
model = DistilBertForSequenceClassification.from_pretrained(MODEL_DIR, device_map=None)
model.to("cpu").eval()

def classify_music_request(text: str) -> str:
    inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True)
    with torch.no_grad():
        logits = model(**{k: v.to("cpu") for k, v in inputs.items()}).logits
        pred = torch.argmax(logits, dim=1).item()
        return model.config.id2label[pred]
