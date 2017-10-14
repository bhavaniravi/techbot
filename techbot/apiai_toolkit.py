import apiai
import random
import json
import requests

CLIENT_ACCESS_TOKEN = "9cbe97e8cea54202bd61be0d0d4721d2"
ai = apiai.ApiAI(CLIENT_ACCESS_TOKEN)

SESSION_ID = str(random.randint(2,999))

def formatString(d):
    msg = ""
    for item in d:
        msg = msg + '<a href="'+item+'">'+d[item]+'</a></br>'
    return msg


def format_message(action,reply_message,outcome):
    """
    formats output message depending on the action
    """
    try:
        if not outcome: raise Exception
        reply_message = reply_message.replace("{ "+action+" }", "\n"+formatString(outcome))
    except Exception:
        reply_message = "I dont quite get that"
    return reply_message

def get_intent_action_entity(response):
    """
    given apiai response returns intent,entity,action
    """
    action = None
    entitiy = None
    try:
        intent = response['result']['metadata']['intentName']
    except KeyError:
        intent = None

    try:
        action = response["result"]["action"]
    except KeyError:
        action = None

    try:
        entitiy = response["result"]["parameters"]
    except KeyError:
        try:
            for context in response["result"]["contexts"]:
                entitiy = context["parameters"]
                break
        except KeyError as e:
            print (e)
            entitiy = None
    return intent,action,entitiy


def send_message(message):
    """
    Sends user text message to api.ai and gets NLU information
    """
    request = ai.text_request()
    request.session_id = SESSION_ID
    request.query = message
    response = request.getresponse()
    raw_response = response.read()
    return json.loads(raw_response.decode())
