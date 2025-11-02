# CS425_G2_T5_project
Weather &amp; Music Chatbot

# Recommended directory for our project
## social-chatbot/
* data/
   * intents_train.json                      # Labeled data for training DistilBERT
   * intents_test.json                       # Holdout data for testing the classifier
* datasets_local/
   * train_AddToPlaylist_full.json           # Downloaded data for training play_music intents
   * train_BookRestaurant_full.json          # Downloaded data for training small_talk intents
   * train_GetWeather_full.json              # Downloaded data for training small_talk intents
   * train_PlayMusic_full.json               # Downloaded data for training play_music intents
   * train_SearchScreeningEvent_full.json    # Downloaded data for training small_talk intents
* models/
  * intent_classifier/                       # Saved DistilBERT model files (tokenizer, weights)
* src/
  * convert_local_dataset.py                 # Code for converting the messy local dataset into trainable json strings
  * stage1_classifier.py                     # Code for loading, training, and running the DistilBERT model (Jaden)
  * stage2_handler.py                        # Contains API connectors, regex logic, and response templates (Vishnu, Kenneth)
  * app.py                                   # The main entry point and Streamlit UI code (Verdio)
* tests/
  * test_functions.py                        # Unit and integration tests (Verdio)
* requirements.txt
* README.md

Output after running stage1_classifier_play_music:

Some weights of DistilBertForSequenceClassification were not initialized from the model checkpoint at distilbert-base-uncased and are newly initialized: ['classifier.bias', 'classifier.weight', 'pre_classifier.bias', 'pre_classifier.weight']
You should probably TRAIN this model on a down-stream task to be able to use it for predictions and inference.
Starting DistilBERT fine-tuning...
  0%|                                                                        | 0/2235 [00:00<?, ?it/s]/Users/jadentyh/Desktop/CS425/CS425_G2_T5_project/.venv/lib/python3.12/site-packages/torch/utils/data/dataloader.py:692: UserWarning: 'pin_memory' argument is set as true but not supported on MPS now, device pinned memory won't be used.
  warnings.warn(warn_msg)
{'loss': 0.1188, 'grad_norm': 0.013790298253297806, 'learning_rate': 1.9960000000000002e-05, 'epoch': 0.67}
 33%|████████████████████▋                                         | 745/2235 [04:11<11:34,  2.15it/s]/Users/jadentyh/Desktop/CS425/CS425_G2_T5_project/.venv/lib/python3.12/site-packages/torch/utils/data/dataloader.py:692: UserWarning: 'pin_memory' argument is set as true but not supported on MPS now, device pinned memory won't be used.
  warnings.warn(warn_msg)
{'loss': 0.0003, 'grad_norm': 0.0029474198818206787, 'learning_rate': 1.4247838616714697e-05, 'epoch': 1.34}
 67%|████████████████████████████████████████▋                    | 1490/2235 [08:18<03:54,  3.18it/s]/Users/jadentyh/Desktop/CS425/CS425_G2_T5_project/.venv/lib/python3.12/site-packages/torch/utils/data/dataloader.py:692: UserWarning: 'pin_memory' argument is set as true but not supported on MPS now, device pinned memory won't be used.
  warnings.warn(warn_msg)
{'loss': 0.0001, 'grad_norm': 0.0015108819352462888, 'learning_rate': 8.484149855907782e-06, 'epoch': 2.01}
{'loss': 0.0, 'grad_norm': 0.0007773281540721655, 'learning_rate': 2.7204610951008647e-06, 'epoch': 2.68}
{'train_runtime': 747.4548, 'train_samples_per_second': 47.822, 'train_steps_per_second': 2.99, 'train_loss': 0.026667745057618458, 'epoch': 3.0}
100%|█████████████████████████████████████████████████████████████| 2235/2235 [12:27<00:00,  2.99it/s]

Model and tokenizer saved to models/intent_classifier
