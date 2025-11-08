import torch  # Imports the core PyTorch deep learning library, required by Hugging Face models.
from datasets import (
    load_dataset,
)  # Tool to easily load and manage datasets from the Hugging Face Hub.
from transformers import (  # Imports necessary components from the Transformers library.
    DistilBertTokenizerFast,  # The fast tokenizer for DistilBERT, used to convert text to numerical IDs.
    DistilBertForSequenceClassification,  # The DistilBERT model adapted for classification tasks.
    Trainer,  # Class that provides a standard API for training models in the Transformers library.
    TrainingArguments,  # Class to hold all the configuration settings for the training process.
)
import os

# --- 1. Configuration ---

MODEL_NAME = "distilbert-base-uncased"  # Specifies the pre-trained model variant to use (uncased means non-case sensitive).
MODEL_DIR = "models/intent_classifier"  # The local directory where the final trained model will be saved.
TRAIN_FILE = "data/intents_train.json"  # Path to the training dataset.
TEST_FILE = "data/intents_test.json"  # Path to the testing/validation dataset.
BATCH_SIZE = 16  # Defines how many samples are processed at once during training (adjust based on GPU memory).
NUM_EPOCHS = 3  # Sets the number of times the training process will iterate over the entire dataset.
LEARNING_RATE = 2e-5  # Defines the size of the steps the model takes to adjust weights during optimization.


# --- 2. Data Loading and Tokenization ---


def load_data():
    """
    Loads both train and test JSON data using Hugging Face Datasets.
    The dataset is returned as a DatasetDict with 'train' and 'test' splits.
    """
    dataset = load_dataset("json", data_files={"train": TRAIN_FILE, "test": TEST_FILE})
    return dataset


def tokenize_function(examples):
    """
    Tokenizes the input text and maps labels to numerical IDs.
    """
    tokenized_inputs = tokenizer(
        examples["text"],  # The column containing the user query text.
        truncation=True,  # Truncate sequences longer than max_length.
        padding="max_length",  # Pad sequences to the specified max_length.
        max_length=128,  # Sets the maximum length for all input sequences.
    )

    # Convert string label (intent) to the corresponding integer ID.
    tokenized_inputs["labels"] = [LABEL_TO_ID[intent] for intent in examples["intent"]]
    return tokenized_inputs


# --- 3. Main Fine-Tuning Block ---

if __name__ == "__main__":

    # Load the tokenizer for DistilBERT
    tokenizer = DistilBertTokenizerFast.from_pretrained(MODEL_NAME)

    # Load dataset (train + test)
    dataset = load_data()

    # Dynamically detect all labels in the dataset instead of hardcoding
    unique_labels = sorted(list(set(dataset["train"]["intent"])))
    LABEL_TO_ID = {
        label: i for i, label in enumerate(unique_labels)
    }  # {'play_music': 0, 'small_talk': 1}
    ID_TO_LABEL = {
        i: label for label, i in LABEL_TO_ID.items()
    }  # {0: 'play_music', 1: 'small_talk'}
    NUM_LABELS = len(unique_labels)  # Should be 2 for this project

    # Apply tokenization to the dataset
    tokenized_dataset = dataset.map(
        tokenize_function,
        batched=True,  # Speeds up processing by batching input samples
        remove_columns=[
            "text",
            "intent",
        ],  # Removes raw text columns to keep only numerical inputs
    )

    # Load the base DistilBERT model and configure classification head
    model = DistilBertForSequenceClassification.from_pretrained(
        MODEL_NAME, num_labels=NUM_LABELS
    )
    model.config.id2label = (
        ID_TO_LABEL  # Attach ID → label mapping for readable predictions
    )
    model.config.label2id = (
        LABEL_TO_ID  # Attach label → ID mapping for training consistency
    )

    # Define training arguments
    training_args = TrainingArguments(
        output_dir="./results",  # Directory for checkpoints and training logs
        num_train_epochs=NUM_EPOCHS,
        per_device_train_batch_size=BATCH_SIZE,
        warmup_steps=500,
        weight_decay=0.01,
        logging_dir="./logs",
        learning_rate=LEARNING_RATE,
    )

    # Initialize the Trainer (handles training loop for us)
    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=tokenized_dataset["train"],  # Training data
        eval_dataset=tokenized_dataset["test"],  # Testing/validation data
    )

    print("Starting DistilBERT fine-tuning...")

    # Train the model
    trainer.train()

    # Save final model + tokenizer for later use in inference/UI
    os.makedirs(MODEL_DIR, exist_ok=True)
    trainer.save_model(MODEL_DIR)
    tokenizer.save_pretrained(MODEL_DIR)

    print(f"\nModel and tokenizer saved to {MODEL_DIR}")
