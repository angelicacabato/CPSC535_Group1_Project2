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

index_mapping = {}
dist = []
# TODO - This function is still in progress
def process_map_data():
    ####Open Street Map Code###
    # pull map data of Fullerton, CA and plot it
    place = {"city": "Fullerton", "state": "California", "country": "USA"}
    G = ox.graph_from_place(place, network_type="drive", truncate_by_edge=True)

    G_simplify = simplify_original_graph(G)

    # create an dictionary to convert index (original_index, convert_index)
    index_mapping = {convert_index: i for i, convert_index in enumerate(G.nodes)}
    file_path = "D://dist.npy" # no need to re-run algorithm except any special requests

    if os.path.exists(file_path):
        dist = np.load(file_path)
    else:
        dist = floyd_warshall(G, index_mapping)
        np.save(file_path, dist)

    shortest_paths = get_shortest_paths(G, dist)

    # Example using built it shortest path function
    origin = 20972501
    dest = 67543020

    original_shortest_path = get_shortest_path(origin, dest, shortest_paths)
    print(f"original shortest path: {original_shortest_path}")

    # compared with the built-in lib
    route = ox.shortest_path(G, origin, dest, weight="length")
    print(f"original shortest path library: {route}")

    fig, ax = ox.plot_graph_route(G, original_shortest_path, route_color='r', route_linewidth=6, node_size=0, bgcolor='k')
    plt.show()

    return None

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