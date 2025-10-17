import json
import os
from datasets import load_dataset
from sklearn.model_selection import train_test_split
import pandas as pd

# --- 1. Configuration ---

# Define your project's core intents
CORE_INTENTS = ['weather_query', 'play_music']
DATA_DIR = 'data'
SNIPS_DATASET_NAME = "DeepPavlov/snips"
TEST_SIZE = 0.2  # 80% for training, 20% for testing
RANDOM_STATE = 42

# Ensure the output directory exists
os.makedirs(DATA_DIR, exist_ok=True)

# # Load the SNIPS dataset from Hugging Face
# # This dataset contains 7 main task intents, which you will simplify
# snips = load_dataset("snips_wit", "default")

# --- 2. Data Preparation Functions ---

def load_and_map_snips():
    """
    Loads the SNIPS dataset, filters the relevant 'GetWeather' intent,
    and maps all other intents to 'small_talk' for a balanced, simplified dataset.
    """
    print(f"Loading SNIPS dataset: {SNIPS_DATASET_NAME}...")
    
    # Load only the 'train' and 'validation' splits for max data.
    # We will do our own random split later.
    snips_data = load_dataset(SNIPS_DATASET_NAME, 'default', split='train+test')
    
    # Convert to Pandas DataFrame for easier manipulation
    df = snips_data.to_pandas()
    print(f"DEBUG: DataFrame columns found: {df.columns.tolist()}")
    
    # Define mapping logic
    def map_intent(intent_name):
        if intent_name == 'GetWeather':
            return 'weather_query'
        # Map all other SNIPS intents (like 'BookRestaurant', 'RateBook', etc.)
        # to 'small_talk' to simulate non-task-specific queries.
        else:
            return 'small_talk'

    print("Mapping SNIPS intents to project intents...")
   # Correction: Use the correct column name 'label' for the intent string
    df['intent'] = df['label'].apply(map_intent)
    df['text'] = df['utterance']
    
    # Filter for the necessary columns and intents
    df_mapped = df[['text', 'intent']]
    print(f"Total SNIPS examples after mapping: {len(df_mapped)}")

    return df_mapped

def generate_manual_data():
    """
    Manually creates examples for 'play_music' (Spotify links)
    and adds more 'small_talk' examples to ensure a solid baseline.
    """
    print("Generating manual data for 'play_music' and 'small_talk'...")
    
    manual_examples = []
    
    # --- play_music examples (Task: Spotify Link) ---
    spotify_url_base = "http://googleusercontent.com/spotify.com/track/12345ABCDE"
    for i in range(100):
        url = f"http://googleusercontent.com/spotify.com/track/{i:03}XYZ"
        manual_examples.append({'text': f"Play this track for me: {url}", 'intent': 'play_music'})
        manual_examples.append({'text': f"Can you queue up this Spotify link? {url}", 'intent': 'play_music'})
        manual_examples.append({'text': f"I want to hear {spotify_url_base} on Spotify.", 'intent': 'play_music'})
    
    # --- Additional small_talk examples ---
    small_talk_phrases = [
        "How are you doing today?", "What is your name?", "Tell me a joke.", 
        "I'm bored, talk to me.", "That's interesting.", "I don't know what to do.",
        "Can you help me with something else?", "Good morning!", "Goodbye.",
        "What time is it now?", "I'm having a great day."
    ]
    for i in range(len(small_talk_phrases) * 10):
        manual_examples.append({'text': small_talk_phrases[i % len(small_talk_phrases)], 'intent': 'small_talk'})
        
    df_manual = pd.DataFrame(manual_examples)
    print(f"Total manual examples generated: {len(df_manual)}")

    return df_manual


def save_dataset_split(df_split, file_name):
    """
    Converts a DataFrame to a list of dictionaries (for easier processing by Hugging Face)
    and saves it as a JSON file.
    """
    data_list = [{'text': row['text'], 'intent': row['intent']} for index, row in df_split.iterrows()]
    file_path = os.path.join(DATA_DIR, file_name)
    
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data_list, f, ensure_ascii=False, indent=4)
    
    print(f"Successfully saved {len(data_list)} examples to {file_path}")


# --- 3. Main Execution Block ---

if __name__ == '__main__':
    
    # Step 1: Load and Map SNIPS data
    df_snips = load_and_map_snips()
    
    # Step 2: Generate Manual data
    df_manual = generate_manual_data()

    # Step 3: Combine datasets
    df_combined = pd.concat([df_snips, df_manual], ignore_index=True)
    
    # Display class distribution before split (good practice)
    print("\n--- Final Dataset Distribution ---")
    print(df_combined['intent'].value_counts())
    print(f"Total examples: {len(df_combined)}")

    # Step 4: Split data into training and testing sets
    # Use stratified split to maintain class balance in both sets
    df_train, df_test = train_test_split(
        df_combined,
        test_size=TEST_SIZE,
        random_state=RANDOM_STATE,
        stratify=df_combined['intent']
    )

    print(f"\nTraining set size: {len(df_train)}")
    print(f"Testing set size: {len(df_test)}")

    # Step 5: Save the splits to the data/ directory
    save_dataset_split(df_train, 'intents_train.json')
    save_dataset_split(df_test, 'intents_test.json')

    print("\nData preparation complete. Files ready for DistilBERT fine-tuning (Step 2.2).")