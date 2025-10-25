import torch # Imports the core PyTorch deep learning library, required by Hugging Face models.
from datasets import load_dataset # Tool to easily load and manage datasets from the Hugging Face Hub.
from transformers import ( # Imports necessary components from the Transformers library.
    DistilBertTokenizerFast, # The fast tokenizer for DistilBERT, used to convert text to numerical IDs.
    DistilBertForSequenceClassification, # The DistilBERT model adapted for classification tasks.
    Trainer, # Class that provides a standard API for training models in the Transformers library.
    TrainingArguments # Class to hold all the configuration settings for the training process.
)
import numpy as np 
import os

# --- 1. Configuration ---

MODEL_NAME = 'distilbert-base-uncased' # Specifies the pre-trained model variant to use (uncased means non-case sensitive).
MODEL_DIR = 'models/intent_classifier' # The local directory where the final trained model will be saved.
DATA_FILE = 'data/play_music_intents_train.json' # Path to the training data file created in the previous step.
NUM_LABELS = 2 # Sets the number of output classes for the classifier (play_music and small_talk).
BATCH_SIZE = 16 # Defines how many samples are processed at once during training (adjust based on GPU memory).
NUM_EPOCHS = 3 # Sets the number of times the training process will iterate over the entire dataset.
LEARNING_RATE = 2e-5 # Defines the size of the steps the model takes to adjust weights during optimization.

# Map string labels to integer IDs (required by the model).
LABEL_TO_ID = {'play_music': 0, 'small_talk': 1} # Maps the intent strings to unique integers (0 and 1).
ID_TO_LABEL = {v: k for k, v in LABEL_TO_ID.items()} # Creates the reverse mapping (ID back to string label).

# --- 2. Data Loading and Tokenization ---

def load_data():
    """Loads JSON data and prepares it for tokenization."""
    # Hugging Face datasets can load JSON directly, using the specified path.
    raw_datasets = load_dataset('json', data_files={'train': DATA_FILE})
    return raw_datasets['train'] # Returns the 'train' split of the loaded dataset object.

def tokenize_function(examples):
    """Tokenizes text and converts labels to IDs."""
    # Tokenize the input text using the DistilBERT tokenizer.
    tokenized_inputs = tokenizer(
        examples['text'], # The column containing the user query text.
        truncation=True, # Truncate sequences longer than max_length.
        padding='max_length', # Pad sequences to the specified max_length.
        max_length=128 # Sets the maximum length for all input sequences.
    )
    
    # Convert string label (intent) to the corresponding integer ID.
    tokenized_inputs["labels"] = [LABEL_TO_ID[intent] for intent in examples["intent"]]
    return tokenized_inputs # Returns the dictionary of tokenized inputs and numerical labels.

# --- 3. Main Fine-Tuning Block ---

if __name__ == "__main__":
    
    # Load the tokenizer
    tokenizer = DistilBertTokenizerFast.from_pretrained(MODEL_NAME) # Initializes the fast tokenizer for DistilBERT.
    
    # Load and preprocess data
    raw_data = load_data() # Calls the function to load the raw data from the JSON file.
    # Applies the tokenization function to the entire raw dataset.
    tokenized_datasets = raw_data.map(
        tokenize_function, 
        batched=True, # Processes multiple examples at once for speed.
        remove_columns=['text', 'intent'] # Removes the original string columns to keep only the numerical inputs/labels.
    )

    # Load the model, specifying the number of labels
    # Loads the pre-trained model and initializes the classification head for 2 classes.
    model = DistilBertForSequenceClassification.from_pretrained(MODEL_NAME, num_labels=NUM_LABELS)
    model.config.id2label = ID_TO_LABEL # Attaches the numerical ID to string label mapping to the model's config.
    model.config.label2id = LABEL_TO_ID # Attaches the string label to numerical ID mapping to the model's config.

    # Define training arguments
    training_args = TrainingArguments(
        output_dir='./results', # Sets the directory where temporary outputs and checkpoints are stored.
        num_train_epochs=NUM_EPOCHS, # Uses the number of epochs defined in the configuration.
        per_device_train_batch_size=BATCH_SIZE, # Uses the batch size defined in the configuration.
        warmup_steps=500, # Initial steps where the learning rate increases slowly.
        weight_decay=0.01, # Regularization technique to prevent overfitting.
        logging_dir='./logs', # Directory for storing training logs (e.g., for TensorBoard).
        learning_rate=LEARNING_RATE # Uses the learning rate defined in the configuration.
    )

    # Initialize the Trainer
    trainer = Trainer(
        model=model, # Passes the loaded DistilBERT model.
        args=training_args, # Passes the defined training arguments.
        train_dataset=tokenized_datasets, # Passes the tokenized, ready-to-use training dataset.
    )

    print("Starting DistilBERT fine-tuning...") # User feedback message.
    # Train the model
    trainer.train() # Executes the main training loop.

    # Save the final model and tokenizer
    os.makedirs(MODEL_DIR, exist_ok=True) # Ensures the model save directory exists.
    trainer.save_model(MODEL_DIR) # Saves the final model weights and configuration.
    tokenizer.save_pretrained(MODEL_DIR) # Saves the tokenizer files (essential for loading the model later).
    print(f"\nModel and tokenizer saved to {MODEL_DIR}") # User confirmation message.