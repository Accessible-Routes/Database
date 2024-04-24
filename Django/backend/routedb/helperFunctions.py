import pickle
import requests
import json
import osmnx as ox
import networkx as nx
from pykml import parser
from math import sin, cos, sqrt, atan2, radians
import coppyGenerate

def readGraphFromFile():
    """
    readGraphFromFile reads the graph from the file and returns it
    input: None
    return: G_loaded: the graph that was read from the file
    """
    with open("/home/dennib2/Database/Django/backend/routedb/graph.p", 'rb') as f: 
        G_loaded = pickle.load(f)
        return G_loaded

def getElevation(tmp_x, tmp_y):
    """
    getElevation takes in a latitude and longitude and returns the elevation at that point
    
    input: 
        tmp_x: the latitude of the point
        tmp_y: the longitude of the point

    return: data['results'][0]['elevation']: the elevation at the point
    """
    url = f'https://api.open-elevation.com/api/v1/lookup?locations={tmp_y},{tmp_x}
    r = requests.get(url)
    data = json.loads(r.content)
    return data['results'][0]['elevation']

def getDistFromLatLon(point1, point2):
    """
    getDistFromLatLon takes in two points and returns the distance between them
    points are in the form (latitude, longitude)
    input:
        point1: the first point
        point2: the second point
    return: distance: the distance between the two points
    """
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
    """
    elevations takes in a graph and adds the elevation to the edges of the graph. This dumps it in the pickle object
    input: RPI: the graph
    return: None
    """
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
    """
    layerGraph takes in a graph and layers the graph based on the elevation
    input: None
    return: None
    """

    north = 42.73201
    south = 42.72492
    east = -73.67119
    west = -73.68663
    custom_filters = ('["footway"~"sidewalk"]["foot"~"designated|yes"]',)
    G = ox.graph_from_place("Rensselaer Polytechnic Institute")
    #G2 = ox.graph_from_place("Rensselaer Polytechnic Institute", custom_filter='["highway"~"steps"]')
    #G = nx.compose(G1, G2)
    ec = []
    for _,_,_,d in G.edges(keys = True, data = True):   
        #print(d['highway'])
        if 'steps' in d['highway']:
            ec.append('y')
        else:
            ec.append('r')
    #ec = ['y' if 'highway"~"steps' in d else 'r' for _, _, _, d in G.edges(keys=True, data=True)]
    for edge in G.edges(keys = True, data=True):
        print(edge)      
    fig, ax = ox.plot_graph(G, bgcolor='k', edge_color=ec,
                            node_size=0, edge_linewidth=0.5,
                            show=True, close=False)

edgePairs = []
def pairNodes(inputNode, stairNodes):
    """
    pairNodes takes in a node and a list of nodes and returns the node that is the closest to the input node
    input: 
        inputNode: the node to compare 
        stairNodes: the list of nodes to compare
    return: 
        i: the node that is the closest to the input node
    """
    for i in stairNodes:
        tmpName = i[0].split(" ")
        if inputNode[0].split(" ")[:-1] == tmpName[:-1] and len(tmpName) == len(inputNode[0].split(" ")) and i[0] != inputNode[0]:
            return i
def bench1():
    """
    bench1 is just a test bench for using the pairNodes function with a kml file from the RPI disabled students club
    """
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
    """
    addWeights adds the weights to the graph based on the distance between the nodes. This is dumped in the Accessiblke Graph pickle object
    input: None
    return: None
    """
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

# addWeights()
# G = coppyGenerate.readGraphFromFile()
# for i in G.edges(data = True):
#     print(i)

layerGraph()
