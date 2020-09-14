import json
def getConfig():
    with open('config.json') as f:
        return json.load(f)