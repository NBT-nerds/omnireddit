import json


def getConfig():
    with open('config.json', 'w') as f:
        return json.load(f)