import json

with open("topics1.json", "r") as file:
    data = json.load(file)
    result = []
    final = []
    for item in data:
        for key in list(item.keys()):
            result.append(item.get(key))

    for arr in result:
        for item in arr:
            final.append(item)

    print(final)