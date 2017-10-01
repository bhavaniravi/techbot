from . models import *

def get_news(entites):
    category = [entity.get("value","") for entity in entites if entity["entity"] == "category"]
    technology = [entity.get("value","") for entity in entites if entity["entity"] == "technology"]
    if technology == "python":
        infos = Info.query.filter(Info.category.in_(category)).limit(5)
        links = [info.link for info in infos]
        return ("Here are top 5 links \n"+"\n".join(links))
    return "I only support python now"
    
def get_event(entities):
    pass

