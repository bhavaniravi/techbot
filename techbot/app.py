from flask import Flask
from flask import render_template,jsonify,request
import requests
import action_methods
from apiai_toolkit import *
from models import app

@app.route('/')
def hello():
    """
    Sample flask hello world
    """
    return render_template('home.html')


@app.route('/chat',methods=["POST"])
def chat():
    """
    chat end point that performs NLU using rasa.ai
    and constructs response from response.py
    """
    message = request.form["text"]
    print (message)
    response = send_message(message)
    if response["status"]["code"] == 200:
        reply_message = response["result"]["fulfillment"]["speech"]
        try:
            intent,action,entitiy = get_intent_action_entity(response)
        except KeyError:
            pass
        print (intent,entitiy,action)
        if action:
            try:
                methodToCall = getattr(action_methods,action)
                outcome = methodToCall(entitiy)
                print ("$$$$$$$$$$$$",outcome)
                reply_message = format_message(action,reply_message,outcome)
            except AttributeError:
                pass
        print (reply_message)
        return jsonify({"status":"success","response":reply_message})

app.config["DEBUG"] = True
if __name__ == "__main__":
    app.run(port=5000)
