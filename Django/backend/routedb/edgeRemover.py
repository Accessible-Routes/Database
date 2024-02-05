import pickle
import requests
import json
def readGraphFromFile():
      with open("/home/dennib2/Database/Django/backend/routedb/graph.p", 'rb') as f: 
            G_loaded = pickle.load(f)
            return G_loaded

def getElevation(start):
    print(start)
    url = f'https://api.open-elevation.com/api/v1/lookup?locations={start["y"]},{start["x"]}'
    payload = open("request.json")
    r = requests.get(url)
    data = json.loads(r.content)
    return data['results'][0]['elevation']

RPI = readGraphFromFile()
for edge in RPI.edges():
    startID, endID = edge
    startNode = RPI.nodes[startID]
    endNode = RPI.nodes[endID]
    startElevation = getElevation(startNode)
    endElevation = getElevation(endNode)
    edge['tags']['elevation'] = abs(endElevation - startElevation)