import pickle
import requests
import json
import osmnx as ox
import networkx as nx
from pykml import parser

def readGraphFromFile():
      with open("/home/dennib2/Database/Django/backend/routedb/graph.p", 'rb') as f: 
            G_loaded = pickle.load(f)
            return G_loaded

def getElevation(tmp_x, tmp_y):
    #url = f'https://api.open-elevation.com/api/v1/lookup?locations={start["y"]},{start["x"]}'
    url = f'https://api.open-elevation.com/api/v1/lookup?locations={tmp_y},{tmpx}'
    r = requests.get(url)
    data = json.loads(r.content)
    print(data)
    return data['results'][0]['elevation']

def elevations(RPI):
    for edge in RPI.edges():
        startID, endID = edge
        startNode = RPI.nodes[startID]
        endNode = RPI.nodes[endID]
        startElevation = getElevation(startNode['x'], startNode['y'])
        endElevation = getElevation(endNode['x'], endNode['y'])

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

layerGraph()


#RPI = readGraphFromFile()

# RPI = ox.add_edge_speeds(RPI,5)
# RPI = ox.add_edge_travel_times(RPI)
# for edge in RPI.edges():
#     startId, endId = edge
#     startNode = RPI.nodes.get(startId, {})
#     endNode = RPI.nodes.get(endId, {})
#     print(startNode)
#     #if 'highway' in startNode:
         
        
#layerGraph()
    #edge['tags']['elevation'] = abs(endElevation - startElevation)