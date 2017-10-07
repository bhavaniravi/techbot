from flask import Flask
from flask import render_template, jsonify, request
from nlu_functions.intent_handler import *
from nlu_functions.intent import intent_mapper, intents,stopwords
# from nltk.corpus import stopwords

app = Flask(__name__)


@app.route('/')
def index_loader():
    """
    :return: rendered index file
    """
    return render_template("home.html")


def actions(query):
    words = query.split()
    intent = ""
    for word in words:
        if word not in stopwords:
            try:
                intent = intent_mapper[word.lower()]
            except:
                pass
    response_text = ""
    try:
        response_text = eval(intents[intent])
    except Exception as e:
        print(e)
        response_text = "Sorry, I'm not trained to answer that question."
    return response_text


@app.route('/chat', methods=["POST"])
def chat():
    """
    chat end point that performs NLU using our custom scripts
    """
    try:
        query = request.form["text"]
        response_text = actions(query)
        # The response tex  t which is sent back to the front end
        # Log the text
        with open("log.txt", "a") as f:
            f.write("\n")
            f.write(query)
            f.write("\n")
            f.write(response_text)
        return jsonify({"status": "success", "response": response_text})
    # Sending the response
    except Exception as e:
        print(e)
        return jsonify({"status": "success", "response": "Sorry I am not trained to do that yet..."})


app.config["DEBUG"] = True
if __name__ == "__main__":
    app.run(port=8000, debug=True)
