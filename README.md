# CS425_G2_T5_project
Weather &amp; Music Chatbot

# Recommended directory for our project
## social-chatbot/
* data/
   * intents_train.json       # Labeled data for training DistilBERT
   * intents_test.json        # Holdout data for testing the classifier
* models/
  * intent_classifier/       # Saved DistilBERT model files (tokenizer, weights)
* src/
  * stage1_classifier.py     # Code for loading, training, and running the DistilBERT model (Jaden)
  * stage2_handler.py        # Contains API connectors, regex logic, and response templates (Vishnu, Kenneth)
  * app.py                   # The main entry point and Streamlit UI code (Verdio)
* tests/
  * test_functions.py        # Unit and integration tests (Verdio)
* requirements.txt
* README.md
