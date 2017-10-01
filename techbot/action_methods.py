from models import Info
import requests
from bs4 import BeautifulSoup
from geopy.geocoders import Nominatim
import json
import random

def get_jobs(technology, location):
    url = "https://www.shine.com/job-search/" + technology + "-jobs-" + "-in-" + location
    r = requests.get(url)
    b = BeautifulSoup(r.text, 'lxml')
    bb = b.find_all('li', {'class': 'search_listing'})
    jobList = {}
    for jobs in bb:
        bbb = BeautifulSoup(str(jobs), 'lxml')
        aa = bbb.find('a', {'class': 'cls_searchresult_a'})
        href = "https://www.shine.com" + aa['href']
        aaa = bbb.find('strong', {'itemprop': 'title'})
        title = (aaa.text.strip())
        jobList[str(href)] = str(title)
    print (jobList)
    return jobList

def get_meetups(technology,location):
    print (location)
    geolocator = Nominatim()
    location = geolocator.geocode(location)
    url = "https://api.meetup.com/find/events?photo-host=public&text=+" + technology + "&key=d1421476f3f654a755b2118c405c74&radius=30&fields=" + technology
    if location:
        url  += "&lon=" + str(location.longitude) + "&lat=" + str(location.latitude)
    r = requests.get(url)
    result = json.loads(r.text)
    return {events['link']:events["name"] for events in random.sample(result, 5 if len(result) > 5 else len(result))}

def get_jobs_meetups(entities):
    technology = entities["technology"]
    location = entities["geo-city"]
    category = entities["category"]
    print (technology,location,category)
    if  category == "jobs":
        return get_jobs(technology,location)
    elif category == "events":
        return get_meetups(technology,location)


def get_info(entities):
    technology = entities["technology"]
    category = entities["category"]
    infos = Info.query.filter(Info.category.like("%"+category+"%")).limit(5)
    return {info.link:info.title for info in infos}
