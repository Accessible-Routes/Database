import pickle
import requests
import json
import osmnx as ox
import networkx as nx
from pykml import parser
from math import sin, cos, sqrt, atan2, radians
import coppyGenerate
def readGraphFromFile():
      with open("/home/dennib2/Database/Django/backend/routedb/graph.p", 'rb') as f: 
            G_loaded = pickle.load(f)
            return G_loaded

def getElevation(tmp_x, tmp_y):
    url = f'https://api.open-elevation.com/api/v1/lookup?locations={tmp_y},{tmp_x}'
    r = requests.get(url)
    data = json.loads(r.content)
    return data['results'][0]['elevation']

def getDistFromLatLon(point1, point2):
    R = 6373.0
    lat1 = radians(float(point1[0]))
    lon1 = radians(float(point1[1]))
    lat2 = radians(float(point2[0]))
    lon2 = radians(float(point2[1]))

    dlon = lon2 - lon1
    dlat = lat2 - lat1

    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    distance = R * c
    return distance

def elevations(RPI):
    for startID, endID, weight, attrDict in RPI.edges(keys = True, data = True):
        startNode = RPI.nodes[startID]
        endNode = RPI.nodes[endID]
        startElevation = getElevation(startNode['x'], startNode['y'])
        endElevation = getElevation(endNode['x'], endNode['y'])
        deltaElevation = abs(endElevation - startElevation)
        attrDict['elevation'] = deltaElevation
    G = RPI
    with open("/home/dennib2/Database/Django/backend/routedb/Accessible_Graph.p", 'wb') as f:
            pickle.dump(G, f)

def layerGraph():
    north = 42.73201
    south = 42.72492
    east = -73.67119
    west = -73.68663
    custom_filters = ('["footway"~"sidewalk"]["foot"~"designated|yes"]',)
    G1 = ox.graph_from_place("Rensselaer Polytechnic Institute")
    G2 = ox.graph_from_place("Rensselaer Polytechnic Institute", custom_filter='["highway"~"steps"]')
    G = nx.compose(G1, G2)
    ec = []
    for _,_,_,d in G.edges(keys = True, data = True):   
        #print(d['highway'])
        if 'steps' in d['highway']:
            ec.append('y')
        else:
            ec.append('r')
    #ec = ['y' if 'highway"~"steps' in d else 'r' for _, _, _, d in G.edges(keys=True, data=True)]
    for edge in G2.edges(keys = True, data=True):
        print(edge)      
    fig, ax = ox.plot_graph(G, bgcolor='k', edge_color=ec,
                            node_size=0, edge_linewidth=0.5,
                            show=True, close=False)

edgePairs = []
def pairNodes(inputNode, stairNodes):
    for i in stairNodes:
        tmpName = i[0].split(" ")
        if inputNode[0].split(" ")[:-1] == tmpName[:-1] and len(tmpName) == len(inputNode[0].split(" ")) and i[0] != inputNode[0]:
            return i
def bench1():
    with open("/home/dennib2/Database/Django/backend/routedb/stairs.kml") as f:
        doc = parser.parse(f).getroot()
        stairNodes = []
        for point in doc.Document.Folder.Placemark:
            coor = point.Point.coordinates.text.split(',')
            coor_name = str(point.name).strip()
            #print(coor_name, coor[0], coor[1])
            stairNodes.append((coor_name, (coor[0], coor[1])))
        for node in stairNodes:
            endNode = pairNodes(node, stairNodes)
            edgePairs.append((node[0], node, endNode))
            #print(node, endNode)


def addWeights():
    G = coppyGenerate.readGraphFromFile()
    for startId, endId, weight, attrDict in G.edges(keys=True, data=True):
        startNode = G.nodes[startId]
        endNode = G.nodes[endId]
        point1 = (startNode['y'], startNode['x'])
        point2 = (endNode['y'], endNode['x'])
        distance = getDistFromLatLon(point1, point2) * 1000 #in meters as opposed to km
        #tmpWeight = sqrt(distance**2 + G.edges[startId, endId, 0]['elevation']**2)
        print(point1, point2)
        print(distance)
        if distance == 0:
             heuristic = 0
        else:
            heuristic = G.edges[startId, endId, 0]['elevation'] / distance
        G[startId][endId][0]['length'] = distance
        attrDict['heuristic'] = heuristic
    with open("/home/dennib2/Database/Django/backend/routedb/Accessible_Graph.p", 'wb') as f:
            pickle.dump(G, f)

addWeights()
G = coppyGenerate.readGraphFromFile()
for i in G.edges(data = True):
    print(i)