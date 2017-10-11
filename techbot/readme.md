# Techbot

A chatbot that gets you tech blogs, news, Projects, modules etc.,

## Description

Techbot uses [Api.ai](http://api.ai) for natural language understanding.
It uses its own DB, meetup and shine.com APIs to get job and event details

### Setup

This application is built using python3.

To install python3 follow the instruction on [python.org website](http://www.python.org)

If not you can create a virtualenv with python3 and use it

1.  Install all required packages  
    `pip install -r requirement.txt`

2. To run the application run  
    `python app.py`

This will run your application.

### Training Your bot

#### Note :: The following steps are to train api.ai with predefined set of data. You can modify it before uploading it.
For your bot to understand natural language you need to train it.

1. Create a account in [Api.ai](http://api.ai)
2. Create a new agent
3. Go to settings > import & export 
4. Import training data `techbot.zip` file
5. Once you import it you have your agent trained to get you meanings and opposites
6. To train it furthuer create new intents, entities etx.,
7. For your training to take effect change `CLIENT_ACCESS_TOKEN` under `apiai_toolkit.py`

### Training bot with new set of data

1. create a text file with all the intents
2. Upload the file under `training` in api.ai
3. Map each entry to an intent

