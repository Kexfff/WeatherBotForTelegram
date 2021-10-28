import json


with open('apikeys.txt', 'r') as file:
    keys = json.loads(file.read())[0]
