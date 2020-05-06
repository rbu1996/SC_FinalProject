import json

alldata = {}

with open('polls/MainData.json') as f:
    for line in f:
        line = json.loads(line.strip())
        alldata[line['newsID']] = line