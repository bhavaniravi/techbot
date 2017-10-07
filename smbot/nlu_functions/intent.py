intents = {"intro": "hello(query)",
           "greet": "hello(query)",
           "get_blogs": "get_blogs(query)",
           "jobs": "job(query)",
           "general": "purpose(query)",
           "event-request": "event_request(query)",
           "stop": "stop(query)"}
intent_mapper = {
    "hi": "intro",
    "hey": "intro",
    "hello": "intro",
    "howdy": "intro",
    "quit": "stop",
    "bye": "stop",
    "end": "stop",
    "exit": "stop",
    "job": "jobs",
    "jobs": "jobs",
    "blog": "get_blogs",
    "blogs": "get_blogs",
    "event": "event-request",
    "events": "event-request",
    "meetup": "event-request",
    "meetups": "event-request",
    "do": "general",
    "function": "general",
    "functions": "general",
    "purpose": "general",

}

stopwords = ["a", "and", "the", "this", "list", "get", "display"]
# print(stopwords)
