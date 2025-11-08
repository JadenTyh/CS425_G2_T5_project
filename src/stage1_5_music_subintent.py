import os
from datasets import load_dataset
from transformers import DistilBertTokenizerFast, DistilBertForSequenceClassification, Trainer, TrainingArguments

MODEL_NAME = "distilbert-base-uncased"
DATA_FILE = "data/music_subintent_train.json"
MODEL_DIR = "models/music_subintent_classifier"

label_list = ["play_track", "recommend_genre", "recommend_artist", "play_mood"]
label_to_id = {label: i for i, label in enumerate(label_list)}
id_to_label = {i: label for i, label in enumerate(label_list)}

def tokenize(batch):
    tokenized = tokenizer(
        batch["text"],
        truncation=True,
        padding="max_length",
        max_length=128
    )
    tokenized["labels"] = [label_to_id[label] for label in batch["label"]]
    return tokenized

if __name__ == "__main__":
    tokenizer = DistilBertTokenizerFast.from_pretrained(MODEL_NAME)

    dataset = load_dataset("json", data_files={"train": DATA_FILE})["train"]
    dataset = dataset.map(tokenize, batched=True, remove_columns=["text", "label"])

    model = DistilBertForSequenceClassification.from_pretrained(MODEL_NAME, num_labels=len(label_list))
    model.config.id2label = id_to_label
    model.config.label2id = label_to_id

    training_args = TrainingArguments(
        output_dir="./music_results",
        num_train_epochs=3,
        per_device_train_batch_size=16,
        learning_rate=2e-5,
        weight_decay=0.01,
        logging_steps=50
    )

    trainer = Trainer(model=model, args=training_args, train_dataset=dataset)
    trainer.train()

    os.makedirs(MODEL_DIR, exist_ok=True)
    trainer.save_model(MODEL_DIR)
    tokenizer.save_pretrained(MODEL_DIR)

    print(f"\nMusic sub-intent classifier saved to {MODEL_DIR}")
