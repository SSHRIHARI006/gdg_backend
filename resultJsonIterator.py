import json
from headerFetcher import getTopicHeader
def getVideoIdRelevant(header):
    videoId = []
    with open("result.json", "r") as file:
        data = json.load(file)
        header_keys = list(header.keys())
        calculate_max = False
        for key in header_keys:
            allVideosIdObj = data.get(key)
            predicate = [list(allVideosIdObj[0].values())[0].get(topic) for topic in header.get(key)]
            if (len(predicate)) == 1:
                tempEmbedding = -100
                videoId = []
                for video in allVideosIdObj:
                    predicate = list(video.values())[0].get(header.get(key)[0])
                    if (predicate > tempEmbedding): 
                        tempEmbedding = predicate
                        if (predicate < 0.5 and predicate > 0):
                            videoId.append(list(video.keys())[0])
            
            else:
                videoId = []
                for video in allVideosIdObj:
                    predicate = [list(video.values())[0].get(item) for item in header.get(key)]
                    pass_bool = bool(predicate[0] > 0)
                    for i in range(len(predicate) - 1):
                        if ((not (predicate[i+1] > 0)) and not (
                            predicate[i + 1] / predicate[i] > 0.7 and predicate[i + 1] / predicate[i] < 1.25
                        )):
                            videoId.append(list(video.keys())[0])
        file.close()
    return videoId
    