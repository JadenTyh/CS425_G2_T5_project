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

to run the project now after pulling / cloning the git
just
1. cd to project root

2. Train the classifier model with
# python src/stage1_classifier_.py
this takes about 45mins for me, might take longer or shorter depending on ur laptop's GPU power

2.5. To test the classifier model, run
# python src/stage1_classifier_test.py
no front end, just in console

3. Train the small_talk model by
# going to google colab, 
# - upload the cs425_small_talk_model as well as data/small_talk_moody_teen_dataset.csv into file location to train it
# after training, uncomment code near the bottom to download the zip file and extract into models/small_talk

4. Train the music_subintent model by running
# python src/stage1_5_music_subintent.py
Might take another 30-50mins

5. Once you've trained all 3 models, you can run the app by 
# streamlit run src/app.py
