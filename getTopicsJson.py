import json
def fetchTopics():
    file = open("topics1.json", "r")
    result = json.load(file)
    file.close()
    return result