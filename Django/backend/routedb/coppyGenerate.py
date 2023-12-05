import json
import math

import geopandas as gpd
import networkx as nx
import osmnx as ox
import pandas as pd
from entrancePoint import entrancePoint

#A test function for plotting a path from 2 seperate nodes in RPI
def testPlotRoute(RPI):
      orig = ox.nearest_nodes(RPI, 42.7324294, -73.6905807)
      dest = ox.nearest_nodes(RPI, 42.7338301, -73.6847063)
      #1208042175, "lat": 42.7268945, "lon": -73.6737245
      route = nx.shortest_path(RPI, orig, dest, 'travel_time')
      return route
#Finds the minimum distance between a node and all other nodes within RPI
#This fucntion was written to fix a few issues when using networkX's closest node function
def closestNode(G, x, y, orig_id):
    #min dist set to infinity representation
    min_dist = float('inf')
    closest_node_id = None
    for node in G.nodes:
        #uses distance formula to determine closest node
        tmp_node = G.nodes[node]
        tmp_x = float(tmp_node['x'])
        tmp_y = float(tmp_node['y'])
        tmp_dist = math.sqrt((tmp_y - y)**2 + (tmp_x - x)**2)
        #sets the closest node id to the closest node is the id is not the same and the distance is not 0
        if tmp_dist < min_dist and orig_id != node and tmp_dist != 0.0:
            # print(f"({x}, {y}) : {orig_id} --> ({tmp_x}, {tmp_y}){tmp_dist} --> {node}")
            closest_node_id = node
            min_dist = tmp_dist
    return closest_node_id
#reads and creates the custom node array in a form that will be accepted bt networkx
def createNodeArray(filename):
      f = open(filename)
      data = json.load(f)
      #this commented out function is meant to seperate sepearate id's for easier locaiton
      #add_nulls = lambda number, zero_count : "{0:0{1}d}".format(number, zero_count)
      counter = 0
      nodeArr = []
      #for each entrance a building has, create an entrancePoint object and serialize it within the nodeArr list
      for i in data['Entrances']:
            for j in i['Points']:
                  counter += 1
                  buidling = i['NAME']
                  tmp_id = counter#add_nulls(counter, 5)
                  pointName = buidling + str(tmp_id)
                  #print(pointName)
                  lat, lon = j.strip(' ').split(',')
                  #print(float(lon), float(lat))
                  tmp_p = entrancePoint(int(tmp_id), lon, lat, pointName, buidling)
                  nodeArr.append(tmp_p.serialize())
      #returns a pandas GeoDataFrame containing the contents of our node array
      gdf = gpd.GeoDataFrame(nodeArr)
      return gdf

#main driver function of generating our connected graph of RPI
def plotGraph(new_nodes):
      ox.settings.log_console = False
      ox.settings.use_cache = True
      #creates the bounding box
      north = 42.73201
      south = 42.72492
      east = -73.67119
      west = -73.68663
      RPI = ox.graph_from_bbox(north, south, east, west, network_type = "walk")
      #adds edge speeds to each edge withing RPI assuming people walk at an average speed of 5km/h
      RPI = ox.add_edge_speeds(RPI,5)
      RPI = ox.add_edge_travel_times(RPI)
      #converts a graph to a geodataframe for adding our new nodes to this dataset
      nodes, edges = ox.graph_to_gdfs(RPI, nodes=True, edges=True)  
      new_node_gdf = gpd.GeoDataFrame(new_nodes)
      #sets the standards for our new nodes data frame
      new_node_gdf = new_node_gdf.set_crs(4326, allow_override=True)
      nodes = nodes.set_crs(4326, allow_override=True)  
      non_new_nodes = nodes  
      #concatinates our two dataframs to put our new nodes at the bottom
      nodes = pd.concat([nodes, new_node_gdf], ignore_index=False)
      entrance_df = nodes[nodes['highway'].str.contains("Entrance", na=False)]
      counter = len(new_nodes)
      new_edge_list = []
      RPI = ox.graph_from_gdfs(nodes, edges)
      #finds the closest node of all nodes that are entrances and adds a bi-directional edge to these two nodes
      for index, row in entrance_df.iterrows():
            tmp_orig_id = int(row['id'])
            tmp_x = float(row['x'])  
            tmp_y = float(row['y'])          
            tmp_dest_id = closestNode(RPI, tmp_x, tmp_y, tmp_orig_id)
            if tmp_orig_id != 33:
                  RPI.add_edge(tmp_dest_id, tmp_orig_id)
                  RPI.add_edge(tmp_orig_id, tmp_dest_id)   
      #adds speeds again
      RPI = ox.add_edge_speeds(RPI,5)   
      G = RPI
      #print(RPI.nodes)
      #saves our graph to a test.graphml file
      ox.save_graphml(G, "test.graphml")
      return RPI

def readGraphFromFile():
      nx.read_graphml("test.graphml")

def routemaker(start, end):
      try:
            place = 'Rensselaer Polytechnic Institute'
            new_nodes = createNodeArray('.\\buildingEntrance.json')
            test = readGraphFromFile()#plotGraph(new_nodes)

            nodes, edges = ox.graph_to_gdfs(test, nodes=True, edges=True) 
            entrance_df = nodes[nodes['highway'].str.contains("Entrance", na=False)]
            start_node = int(entrance_df.loc[entrance_df['highway'] == start]['id'].values[0].item())
            end_node = int(entrance_df.loc[entrance_df['highway'] == end]['id'].values[0].item())

            route = nx.shortest_path(test, start_node, end_node, 'travel_time')
            # #shortest_path = nx.shortest_path(test, source=start_node, target=end_node)

            route_list = []
            for i in route:
                  node = {}
                  node['latitude'] = test.nodes[i]['y']
                  node['longitude'] = test.nodes[i]['x']
                  route_list.append(node)
      
            return route_list[1:-1]
      except:
            return [] 

#ox.save_graphml(test, filepath)
#G = ox.load_graphml(filepath)
      