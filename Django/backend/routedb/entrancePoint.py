from shapely.geometry import  Point
import geopandas as gpd
import pandas as pd
import numpy as np

class entrancePoint:
      """
      This class is used to create an entrance point object for RPI buildings. This information is used to create a GeoDataFrame object for the entrance points of the buildings.
      It is then added to the networkX graph as a node and is paired with a cooresponding node on the graph. This edge is then given a weight of 0 to represent it as an entrance.
      init: id, lng, lat, name, building
      """
      def __init__(self, id, lng, lat, name, building):
            self.type = 'node'
            self.id = id
            self.lng = lng
            self.lat = lat
            self.tags = {"Entrance" : "Entrance_" + building}
    
      def serialize(self):
            """
            serialize: This function is used to serialize the entrance point object into a dictionary
            This function is used to convert the class object into a dictionary for storage in the networkX graph as networkX operates as a dictinary of dictionaries of dictionaries
            """
            dict ={
                  'id' : self.id,
                  'y' : self.lat,
                  'x' : self.lng,
                  'highway' : self.tags['Entrance'],
                  'street_count' : 1,
                  'geometry' : Point(self.lng, self.lat),
                  'osmid' : self.id,
            }
            return dict
