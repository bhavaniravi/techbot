from flask import Flask
from flask import render_template,jsonify,request
import requests
from .models import *
import random
from . import intentResponse

@app.route('/')
def hello_world():
    """
    Sample hello world
    """
    return render_template("home.html")



@app.route('/chat',methods=["POST"])
def chat():
    """
    chat end point that performs NLU using rasa.ai
    and constructs response from response.py
    """
    try:
        response = requests.get("http://localhost:5000/parse",params={"q":request.form["text"]})
        response = response.json()
        intent = response["intent"]["name"]
        entities = response["entities"]
        print (intent)
        print ("Entites",entities)
        response_text = getattr(intentResponse, intent)(entities)
        return jsonify({"status":"success","response":response_text})
    except Exception as e:
        print (e)
        return jsonify({"status":"success","response":"Sorry I am not trained to do that yet..."})


app.config["DEBUG"] = True
if __name__ == "__main__":
    app.run(port=8000)
