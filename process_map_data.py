"""
GROUP 1: Anunay Amrit, Angelica Cabato, Pranav Vijay Chand, Riya Chapatwala, Sai Satya Jagannadh Doddipatla, Nhat Ho

Dr. Shah

CPSC 535: Advanced Algorithms (Spring 2024)

"""

# Reference Option #1: https://www.geeksforgeeks.org/working-with-geospatial
# -data-in-python/

# Reference Option #2: https://networkx.org/documentation/stable/auto_examples/geospatial/plot_osmnx.html

###### Imports needed for Open Street Map API ######
import networkx as nx
import osmnx as ox
import geopandas as gpd
import matplotlib.pyplot as plt
from floyd_warshall import floyd_warshall
import numpy as np
import os
import pandas as pd
import shapely
from shapely.geometry import Point, Polygon

index_mapping = {}
dist = []
cafe_dict = {}
nearest_node_cafes = {} # Node osmid : idx for shortest path matrix
updated_nodes = []
updated_edges = []

def process_map_data():
    ####Open Street Map Code###
    # pull map data of Fullerton, CA
    place = {"city": "Fullerton", "state": "California", "country": "USA"}
    G = ox.graph_from_place(place, network_type="drive", truncate_by_edge=True)

    nodes, edges = ox.graph_to_gdfs(G)

    # get building information
    fullerton_cafes = ox.features_from_place(place,
                                                 tags={"amenity": "cafe"})

    G_simplify = simplify_original_graph(G)

    # populate dictionary of cafes in Fullerton
    create_cafe_dict(cafe_dict, fullerton_cafes)
    print(cafe_dict['Starbucks'])
    print(cafe_dict['7 Leaves Cafe'])

    #example of getting the nearest_node
    orig = 0
    orig = ox.nearest_nodes(G, 33.8602673,-117.942165 , return_dist=False)
    dest = 0
    dest = ox.nearest_nodes(G, 33.8747911, -117.8900264,return_dist=False)
    print(orig)
    print(dest)


    """
    # create an dictionary to convert index (original_index, convert_index)
    index_mapping = {convert_index: i for i, convert_index in enumerate(G.nodes)}
    file_path = "D://dist.npy" # no need to re-run algorithm except any special requests

    if os.path.exists(file_path):
        dist = np.load(file_path)
    else:
        dist = floyd_warshall(G, index_mapping)
        np.save(file_path, dist)

    print(type(index_mapping))
    shortest_paths = get_shortest_paths(G, dist)

    # Example using built it shortest path function
    origin = 414535257
    dest = 1850729215

    #original_shortest_path = get_shortest_path(origin, dest, shortest_paths)
    #print(f"original shortest path: {original_shortest_path}")

    fig, ax = ox.plot_graph_route(G, route, route_color='r', route_linewidth=6,
                                  node_size=0, bgcolor='k')
    plt.show()
"""
    return None

def nearest_node_cafes(nodes, cafe_dict):
  num_vertices = len(nodes)

  for i in range(num_vertices):
    nodeid = nodes.iloc[i].name
    idx = i
    nodeid_dict[nodeid] = idx

  return

# populates cafe_dict structure
def create_cafe_dict(cafe_dict, fullerton_cafes):
    num_cafes = len(fullerton_cafes)

    for i in range(num_cafes):
        name = fullerton_cafes.iloc[i]['name']
        if not pd.isna(name):  # Ignoring features that do not have a name
            osmid = fullerton_cafes.iloc[i].name[1]
            coordinates = fullerton_cafes.iloc[i]['geometry']  # get coordinates
            if type(coordinates) == shapely.geometry.polygon.Polygon: #
                # Ignoring features that have multiple locations
                continue
            else:
                cafe_dict[name] = [osmid, coordinates]
        else:
            continue

    # extract coordinates and repopulate dictionary
    for key in cafe_dict:
        id = cafe_dict[key][0]
        coordinates = cafe_dict[key][1]  # get coordinates
        coordinates = list(
            coordinates.coords)  # get coordinates Geometry is backwards
        Y = coordinates[0][0]
        X = coordinates[0][1]
        cafe_dict[key] = [id, X, Y]


    return cafe_dict

def get_shortest_paths(G, dist):
    num_nodes = len(G.nodes)
    shortest_paths = {}
    for i in range(num_nodes):
        shortest_paths[i] = {}
        for j in range(num_nodes):
            shortest_paths[i][j] = dist[i, j]
    return shortest_paths

# need to re-check
def get_shortest_path(orgin, dest, shortest_paths):
    global index_mapping
    mapped_orig, mapped_dest = index_mapping[orgin], index_mapping[dest]
    shortest_path_length = shortest_paths[mapped_orig][mapped_dest]
    if np.isinf(shortest_path_length):
        return None
    
    path = [dest]
    while dest != orgin:
        for node, matrix_index in index_mapping.items():
            if dist[mapped_orig, matrix_index] + dist[matrix_index, mapped_dest] == shortest_path_length and dist[mapped_orig, matrix_index] != np.inf:
                path.insert(0, node)
                dest = node
                break

    return path

# convert string input from UI then convert to numeric value
def convertLocation2Numeric(source, destination):
    return source, destination

# based on the list to simplify the original graph
def simplify_original_graph(graph):
    return graph