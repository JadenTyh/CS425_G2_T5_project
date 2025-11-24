# CS425_G2_T5_project
Weather Music Movies Chatbot

to run the project now after pulling / cloning the git
just
1. cd to project root

2. create training and testing intents with
# python src/stage0_convert_local_dataset.py

3. Train the classifier model with
# python src/stage1_classifier_.py
this takes about 45mins for me, might take longer or shorter depending on ur laptop's GPU power

3.5. To test the classifier model, run
# python src/stage1_classifier_test.py
no front end, just in console

4. Train the small_talk model by
# going to google colab, 
# - upload the cs425_small_talk_model as well as data/small_talk_moody_teen_dataset.csv into file location to train it
# after training, uncomment code near the bottom to download the zip file and extract into models/small_talk

5. Train the music_subintent model by running
# python src/stage1_5_music_subintent.py
Might take another 30-50mins

6. Once you've trained all 3 models, you can run the app by 
# streamlit run src/app.py
