import json
import os
from glob import glob
from sklearn.model_selection import train_test_split

DATASET_DIR = "datasets_local"
OUTPUT_DIR = "data"
os.makedirs(OUTPUT_DIR, exist_ok=True)

def load_json_file(filepath):
    """Load SNIPS local dataset in any format and flatten text fragments safely."""
    
    # Try UTF-8, fallback to Latin-1
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            raw = json.load(f)
    except UnicodeDecodeError:
        with open(filepath, "r", encoding="latin-1") as f:
            raw = json.load(f)

    samples = []

    # Case 1: SNIPS benchmark format → { "PlayMusic": [ { "data": [...] }, ... ] }
    if isinstance(raw, dict):
        for intent_name, utterances in raw.items():
            if not isinstance(utterances, list):
                continue
            for sample in utterances:
                if "data" in sample:
                    text = "".join([segment["text"] for segment in sample["data"]])
                    samples.append((text, intent_name))

    # Case 2: Already flattened format → [ { "text": "...", "intent": "..." }, ... ]
    elif isinstance(raw, list):
        for sample in raw:
            if "text" in sample and "intent" in sample:
                samples.append((sample["text"], sample["intent"]))

    return samples


def map_intent(intent_name):
    """Normalize intent labels to project label schema."""
    intent_name = intent_name.lower()
    if intent_name in ["playmusic", "addtoplaylist"]:
        return "play_music"
    return "small_talk"


print("🔍 Loading dataset from:", DATASET_DIR)

all_data = []
filepaths = sorted(glob(os.path.join(DATASET_DIR, "*.json")))

for filepath in filepaths:
    print(f"➡️  Processing: {filepath}")
    intent_samples = load_json_file(filepath)
    all_data.extend(intent_samples)

print(f"\n📦 Total raw examples loaded: {len(all_data)}")


# Apply label mapping
final_data = [{"text": text, "intent": map_intent(intent)} for text, intent in all_data]

# Train-test split
train_data, test_data = train_test_split(final_data, test_size=0.2, random_state=42)

# Save output
with open(os.path.join(OUTPUT_DIR, "intents_train.json"), "w", encoding="utf-8") as f:
    json.dump(train_data, f, indent=4)

with open(os.path.join(OUTPUT_DIR, "intents_test.json"), "w", encoding="utf-8") as f:
    json.dump(test_data, f, indent=4)

print("\n✅ Dataset successfully built!")
print(f"🎵 play_music examples: {len([x for x in final_data if x['intent']=='play_music'])}")
print(f"💬 small_talk examples: {len([x for x in final_data if x['intent']=='small_talk'])}")
print(f"📚 Train size: {len(train_data)}")
print(f"🧪 Test size:  {len(test_data)}")
print(f"📁 Saved to: {OUTPUT_DIR}/intents_train.json and intents_test.json")
