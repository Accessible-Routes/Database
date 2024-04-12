import json
import math

import geopandas as gpd
import networkx as nx
import osmnx as ox
import pickle
import pandas as pd
from entrancePoint import entrancePoint


"""
testPlotRoute(MultiDiGraph RPI)
This function is used to test the plotRoute function. 
It is not used in the final implementation of the project.
Parameters: RPI - the graph of RPI
"""
def testPlotRoute(RPI):
      
      orig = ox.nearest_nodes(RPI, 42.7324294, -73.6905807)
      dest = ox.nearest_nodes(RPI, 42.7338301, -73.6847063)
      #1208042175, "lat": 42.7268945, "lon": -73.6737245
      route = nx.shortest_path(RPI, orig, dest, 'travel_time')
      return route

"""
closestNode(MultiDiGraph G, int x, int y, int orig_id)
This function is used to find the closest node to a given point.
Parameters: G - the graph of RPI, 
            x - the x coordinate of the point, 
            y - the y coordinate of the point, 
            orig_id - the id of the original node
"""
def closestNode(G, x, y, orig_id):
    min_dist = float('inf')
    closest_node_id = None
    for node in G.nodes:
        tmp_node = G.nodes[node]
        tmp_x = float(tmp_node['x'])
        tmp_y = float(tmp_node['y'])
        tmp_dist = math.sqrt((tmp_y - y)**2 + (tmp_x - x)**2)

        if tmp_dist < min_dist and orig_id != node and tmp_dist != 0.0:
            # print(f"({x}, {y}) : {orig_id} --> ({tmp_x}, {tmp_y}){tmp_dist} --> {node}")
            closest_node_id = node
            min_dist = tmp_dist
    return closest_node_id

"""
createNodeArray(string filename)
This function is used to create a list of entrance points from a json file.
Parameters: filename - the name of the json file
This function calls the class entrancePoint from entrancePoint.py
"""
def createNodeArray(filename):
      f = open(filename)
      data = json.load(f)
      #add_nulls = lambda number, zero_count : "{0:0{1}d}".format(number, zero_count)
      counter = 0
      nodeArr = []
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
      gdf = gpd.GeoDataFrame(nodeArr)
      return gdf

"""
plotGraph(GeoDataFrame new_nodes)
This function is used to plot the graph of RPI with the new nodes added.
Parameters: new_nodes - the new nodes to be added to the graph
This function is used to generate a barebones graph of RPI with the new nodes added as entrances
"""
def plotGraph(new_nodes):
      ox.settings.log_console = False
      ox.settings.use_cache = True
      north = 42.73201
      south = 42.72492
      east = -73.67119
      west = -73.68663
      RPI = ox.graph_from_bbox(north, south, east, west, network_type = "walk")
      #, infrastructures = ('way["highway"~"footway|pedestrian|cycleway|path|living_street|tertiary|unclassified|residental|service"]',))
      RPI = ox.add_edge_speeds(RPI,5)
      RPI = ox.add_edge_travel_times(RPI)
      nodes, edges = ox.graph_to_gdfs(RPI, nodes=True, edges=True)  
      new_node_gdf = gpd.GeoDataFrame(new_nodes)
      new_node_gdf = new_node_gdf.set_crs(4326, allow_override=True)
      nodes = nodes.set_crs(4326, allow_override=True)  
      nodes = pd.concat([nodes, new_node_gdf], ignore_index=False)
      entrance_df = nodes[nodes['highway'].str.contains("Entrance", na=False)]
      RPI = ox.graph_from_gdfs(nodes, edges)
      edgesToRemove = []
      for a, b,_,d in RPI.edges(keys = True, data = True):
            if 'highway' in d.keys():
                  if 'steps' in d['highway']:
                        edgesToRemove.append((a, b))
            if 'length' not in d.keys():
                  d['length'] = 0
      for i in edgesToRemove:
            print(i[0], i[1])
            RPI.remove_edge(i[0], i[1])
      for _, row in entrance_df.iterrows():
            tmp_orig_id = int(row['id'])
            tmp_x = float(row['x'])  
            tmp_y = float(row['y'])          
            tmp_dest_id = closestNode(RPI, tmp_x, tmp_y, tmp_orig_id)
            if tmp_orig_id != 32:
                  RPI.add_edge(tmp_dest_id, tmp_orig_id)
                  RPI.add_edge(tmp_orig_id, tmp_dest_id)   
      RPI = ox.add_edge_speeds(RPI,5)   
      for a, b,_,d in RPI.edges(keys = True, data = True):
            if 'length' not in d.keys():
                  d['length'] = 0
      G = RPI

      
      #ox.plot_graph(G)
      with open("Accessible_Graph.p", 'wb') as f:
            pickle.dump(G, f)
      route = ox.shortest_path(G, 6, 9)
      print(route)
      _, _ = ox.plot_graph_route(G, route, route_color='r', route_linewidth=6, node_size=5)
      return RPI

"""
readGraphFromFile() -> MultiDiGraph
This function is used to read the graph from a file. This is a preset path as django needs a preset path
returns a MultiDiGraph object
"""
def readGraphFromFile():
      with open("~/routedb/Accessible_Graph.p", 'rb') as f: 
            G_loaded = pickle.load(f)
            for i in G_loaded.edges(keys = True, data = True):
                  print(i)
            return G_loaded
      
"""
bensRoute(string start, string end) -> list
This function is used to find the shortest path between two entrances.
This is more a test function and is not used in the final implementation of the project. route is printed to the console
"""
def bensRoute(start, end):
      try:
            place = 'Rensselaer Polytechnic Institute'
            test = readGraphFromFile()
            nodes, edges = ox.graph_to_gdfs(test, nodes=True, edges=True) 
            entrance_df = nodes[nodes['highway'].str.contains("Entrance", na=False)]
            start_node = int(entrance_df.loc[entrance_df['highway'] == start]['id'].values[0].item())
            end_node = int(entrance_df.loc[entrance_df['highway'] == end]['id'].values[0].item())
            route = nx.shortest_path(test, start_node, end_node, weight = 'length')
      
            route_list = []
            for i in route:
                 route_list.append(i)
            for i in range(len(route_list)-1):
                  a = test.get_edge_data(route_list[i], route_list[i+1])[0]
                  print(route[i])
            ox.plot_graph(test)
            return route_list
      except Exception as e:
            print('exception', e)
            return []
      

"""
routemaker(string start, string end) -> list
This function is used to find the shortest path between two entrances.
Parameters: start - the starting entrance, end - the ending entrance
"""
def routemaker(start, end):
      try:
            place = 'Rensselaer Polytechnic Institute'
            test = readGraphFromFile()
            nodes, edges = ox.graph_to_gdfs(test, nodes=True, edges=True) 
            entrance_df = nodes[nodes['highway'].str.contains("Entrance", na=False)]
            start_node = int(entrance_df.loc[entrance_df['highway'] == start]['id'].values[0].item())
            end_node = int(entrance_df.loc[entrance_df['highway'] == end]['id'].values[0].item())
            route = nx.shortest_path(test, start_node, end_node, 'travel_time')     
            route_list = []
            for i in route:
                  node = {}
                  node['latitude'] = test.nodes[i]['y']
                  node['longitude'] = test.nodes[i]['x']
                  route_list.append(node)
            
            return route_list[1:-1]
      except Exception as e:
            print('exception', e)
            return []


if __name__ == "__main__":
      readGraphFromFile()
      new_nodes = createNodeArray('/home/dennib2/Database/Django/backend/routedb/buildingEntrance.json')
      plotGraph(new_nodes)
      testRoute = bensRoute("Entrance_West Hall", "Entrance_Academy Hall")
      print(testRoute)
