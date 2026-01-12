# CS425_G2_T5_project
Weather Music Movies Chatbot

## Setup Instructions

To run the project after pulling/cloning the git repository:

### 1. Navigate to project root
```bash
cd <project-root>
```

### 2. Create training and testing intents
```bash
python src/stage0_convert_local_dataset.py
```

### 3. Train the classifier model
```bash
python src/stage1_intent_classifier.py
```
> **Note:** This takes about 45 minutes.  Duration may vary depending on your laptop's GPU power. 

### 3.5. Test the classifier model (optional)
```bash
python src/stage1_intent_classifier_test. py
```
> No front end, just runs in console. 

### 4. Train the small_talk model
1. Go to [Google Colab](https://colab.research.google.com/)
2. Upload `cs425_small_talk_model` as well as `data/small_talk_moody_teen_dataset. csv` into the file location to train it
3. After training, uncomment code near the bottom to download the zip file
4. Extract the downloaded zip into `models/small_talk`

### 5. Train the music_subintent model
```bash
python src/stage1_5_music_subintent. py
```
> **Note:** This might take another 30-50 minutes.

### 6. Run the app
Once you've trained all 3 models, you can run the app:
```bash
streamlit run src/app.py
```
