import json
from getTopicsJson import fetchTopics

def getTopicHeader(topics):
    result = {}
    for item in fetchTopics():
        search_topics_list = list(item.values())[0]
        for topic in topics:
            if topic in search_topics_list:
                keyObj = list(item.keys())[0]
                if (result.get(keyObj) == None):
                    result[keyObj] = (topic,)
                else:
                    result[keyObj] = (topic, *result[keyObj])

    return result