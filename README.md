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
  * intent_classifier/                       # Saved DistilBERT model files (tokenizer, weights) empty, need to train
* src/
  * convert_local_dataset.py                 # Code for converting the messy local dataset into trainable json strings
  * stage1_classifier.py                     # Code for loading, training, and running the DistilBERT model (Jaden)
  * stage2_handler.py                        # Contains API connectors, regex logic, and response templates (Vishnu, Kenneth)
  * app.py                                   # The main entry point and Streamlit UI code (Verdio)
* tests/
  * test_functions.py                        # Unit and integration tests (Verdio)
* requirements.txt
* README.md
