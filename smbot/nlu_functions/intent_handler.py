import random
from nlu_functions.entity import extract_entity_names
import requests
from geopy.geocoders import Nominatim
import json
from bs4 import BeautifulSoup


def hello(query):
    """
    handles a few predefined hello words
    :param query: The query
    :return: greet text
    """
    if len(query.split()) < 3:
        msg = random.choice(["Hi", "Hey there, how may I help you today", "Hello", "What\'s up!", "Bonjour"])
    else:
        msg = '''Hello, I am A Bot. Ask me what I do!'''
    return msg


def purpose(query):
    """
    Tells the use about the function of the bot
    :param query: The query
    :return: Gives the functionality of the bot
    """
    msg = "Hi, I can give you the following information "
    # Created object for the entity extractor
    entityList = extract_entity_names(query)
    # Got th entity list
    with open("nlu_functions/tech_terms.json", "r") as f:
        tech_terms = f.read()
    terms = json.loads(tech_terms)
    for entity in entityList:
        if entity in terms:
            msg = msg + "about " + str(entity)
            msg = msg + "\n1.Give you python blogs\n2.Give you latest job posting in any location\n3.Give you latest events using meetup API"
            return msg
    msg = msg + "\n1.Give you blogs\n2.Give you latest job posting\n3.Give you latest events in your city"
    return msg


def formatString(d):
    """
    Formats a dictionary into html content
    :param d: dictionary containing link and title
    :return: html formatted text
    """
    msg = ""
    for item in d:
        msg = msg + '<a href="' + item + '" target="_blank">' + d[item] + '</a></br>'
    return msg


def get_blogs(query):
    """
    Takes random 5 blogs from a json file and shows it
    :param query: The queried sentence
    :return: formatted sentence
    """
    # query = query.split()
    # query[len(query) - 1] = query[len(query) - 1].title()
    # query = " ".join(query)
    entityList = extract_entity_names(query)
    d = {}
    msg = ""
    # if "python" in entityList:
    with open("nlu_functions/blogs.json", "r") as f:
        raw_blog = f.read()
        blogs = json.loads(raw_blog)
        msg = msg + "We found five blogs that suit your query</br>"
        count = 0
        # taking random 5 from the dictionary
        keys = random.sample(list(blogs.keys()), 5)
        for item in keys:
            count = count + 1
            d[item] = blogs[item]
            if count == 5:
                break
        msg = msg + formatString(d)

    return msg


def get_languages(entityList):
    """
    Extracts the first tech term from a json file and display it
    :param entityList: The list of entities
    :return: The first tech term found in the json file
    """
    with open("nlu_functions/tech_terms.json", "r") as f:
        tech_terms = f.read()
    terms = json.loads(tech_terms)
    for entity in entityList:
        if entity in terms:
            return entity
    return ""


def get_jobs(entityList):
    """
    Calls shine.com and scrapes the data
    :param entityList: List of entities
    :return: List of jobs with their links
    """
    with open("nlu_functions/tech_terms.json", "r") as f:
        tech_terms = f.read()
    with open("nlu_functions/cities.json", "r") as f:
        raw_cities = f.read()
    cities = set(json.loads(raw_cities))
    city = ""
    terms = json.loads(tech_terms)
    jobList = {}
    for entity in entityList:
        if entity.title() in cities:
            city = entity
    for entity in entityList:
        if entity in terms:
            if city == "":
                url = "https://www.shine.com/job-search/" + entity + "-jobs-"
            else:
                url = "https://www.shine.com/job-search/" + entity + "-jobs-" + "in-" + city
            r = requests.get(url)
            print(url)
            # getting the page content
            soup = BeautifulSoup(r.text, 'lxml')
            # extracting usefull data
            searchList = soup.find_all('li', {'class': 'search_listing'})
            for jobs in searchList:
                soup_2 = BeautifulSoup(str(jobs), 'lxml')
                link = soup_2.find('a', {'class': 'cls_searchresult_a'})
                href = "https://www.shine.com" + link['href']
                p = soup_2.find('strong', {'itemprop': 'title'})
                title = (p.text.strip())
                jobList[str(href)] = str(title)
    # print(type(jobList))
    return jobList


def job(query):
    """
    A helper function that calls get_jobs(), gets the data and sends it back to the frontend
    :param query: User requested query
    :return: formatted message with just 5 inputs
    """
    entityList = extract_entity_names(query)
    if len(entityList) < 2:
        return "Kindly add a job parameter"
    jobs = get_jobs(entityList)
    msg = ""
    d = {}
    if len(jobs) > 5:
        msg = msg + "We found 5 links that match your query</br>"
        # randomly selecting 5 jobs
        keys = random.sample(jobs.keys(), 5)
        # print("Keys:" + keys)
        for item in keys:
            d[item] = jobs[item]
        msg = msg + formatString(d)
    elif len(jobs) == 0:
        msg = "Sorry couldn't find a job for you :("
    else:
        msg = msg + "We found " + str(len(jobs)) + " links that match your query</br>"
        for item in jobs.keys():
            d[item] = jobs[item]
        msg = msg + formatString(d)
    print(msg)
    return msg


def stop(query):
    return "See you soon"


def get_city(entityList):
    """
    Return the Indian city from a list of entities
    :param entityList: entity list
    :return: The Indian city that exists in cities.json
    """
    with open("nlu_functions/cities.json", "r") as f:
        city = set(json.loads(f.read()))
    for entity in entityList:
        if entity.title() in city:
            return entity.title()
    return ""


def event_request(query):
    """
    Queries the meetup Api and returns a list of 5 randomly selected events
    :param query: The input stirng
    :return: Formatted html string of 5 randomly selected meetup's
    """
    entityList = extract_entity_names(query)
    # print(entityList)
    if len(entityList) == 0:
        return "Sorry! I didn't understand!"
    language = get_languages(entityList)
    place = get_city(entityList)
    if place != "":
        # meetup api needs the lat and long for a place
        geolocator = Nominatim()
        location = geolocator.geocode(place)
        long = location.longitude
        lat = location.latitude
    else:
        long = ""
        lat = ""
    if lat == "":
        url = "https://api.meetup.com/find/events?photo-host=public&text=+" + language + "&key=d1421476f3f654a755b2118c405c74&radius=30&fields=" + language
    else:
        url = "https://api.meetup.com/find/events?photo-host=public&text=+" + language + "&key=d1421476f3f654a755b2118c405c74&radius=30&fields=" + language + "&lon=" + str(
            long) + "&lat=" + str(lat)
    r = requests.get(url)
    print(url)
    # dictionary to store the links and the title
    d = {}
    msg = ""
    meetups = json.loads(r.text)
    if len(meetups) == 0:
        msg = "Sorry dude! No events found for your query!"
    else:
        if len(meetups) > 5:
            msg = msg + "We found 5 links that match your query</br>"
            for events in random.sample(meetups, 5):
                d[events['link']] = events['name']
        else:
            msg = msg + "We found " + str(len(meetups)) + " links that match your query</br>"
            for events in meetups:
                d[events['link']] = events['name']
        msg = msg + formatString(d)
    return msg
