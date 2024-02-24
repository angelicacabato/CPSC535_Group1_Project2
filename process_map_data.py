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

def process_map_data(source_location=None, destination_location=None,fetch_cafes_only=False,
                     blockages=None, cafeLocations=None):
    ####Open Street Map Code###

    if blockages is None:
            blockages = []
    if cafeLocations is None:
            cafeLocations = {}

    # pull map data of Fullerton, CA
    place = {"city": "Fullerton", "state": "California", "country": "USA"}
    G = ox.graph_from_place(place, network_type="drive", truncate_by_edge=True)

    # Refresh graph to reflect blockages accurately
    G = apply_blockages_to_graph(G, blockages, cafeLocations)

    if fetch_cafes_only:

        fullerton_cafes = ox.features_from_place(place,
                                                    tags={"amenity": "cafe"})

        G_simplify = simplify_original_graph(G)
        # populate dictionary of cafes in Fullerton
        create_cafe_dict(cafe_dict, fullerton_cafes)
        # Convert cafe_dict to a list format for the frontend
        cafe_list = [{"name": name, "id": cafe_info[0], "lat": cafe_info[1], "lng": cafe_info[2]} for name, cafe_info in cafe_dict.items()]
        return None, cafe_list   
    
    if source_location and destination_location:
        nearest_source_node = ox.nearest_nodes(G, source_location[1], source_location[0])
        nearest_destination_node = ox.nearest_nodes(G, destination_location[1], destination_location[0])
        route = ox.shortest_path(G, nearest_source_node, nearest_destination_node, weight='length')
        route_latlon = [(G.nodes[node]['y'], G.nodes[node]['x']) for node in route]
        return route_latlon
    
def apply_blockages_to_graph(G, blockages, cafeLocations):
    for blockage in blockages:
        source = cafeLocations.get(blockage[0])
        destination = cafeLocations.get(blockage[1])
        if source and destination:
            source_node = ox.nearest_nodes(G, source[1], source[0])
            destination_node = ox.nearest_nodes(G, destination[1], destination[0])
            if G.has_edge(source_node, destination_node):
                # Increase the weight of the edge significantly
                G[source_node][destination_node][0]['length'] = 1e9
            if G.has_edge(destination_node, source_node):
                G[destination_node][source_node][0]['length'] = 1e9
    return G

    #fig, ax = ox.plot_graph_route(G, route, route_color='r',
    # route_linewidth=6, node_size=0, bgcolor='k')

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

    # compared with the built-in lib
    route = ox.shortest_path(G, origin, dest, weight="length")
    print(f"original shortest path library: {route}")

    #fig, ax = ox.plot_graph_route(G, original_shortest_path, route_color='r',
                                # route_linewidth=6, node_size=0, bgcolor='k')
    plt.show()
    """
    # return None

################## Helper Functions ################################

def get_nearest_nodes(G, cafe_dict, nodes, nearest_node_cafes):
    # print nearest nodes - x and y must be flipped for call to work
    nodes_to_keep = []
    nodes_to_keep_id = []
    for cafe_name, cafe_info in cafe_dict.items():
        Y = cafe_info[1]
        X = cafe_info[2]
        nearest_node = ox.nearest_nodes(G, X, Y,
                                        return_dist=False)
        nodes_to_keep.append(nearest_node)
        print(f"Nearest node to {cafe_name}: {nearest_node}")

    for id in nodes_to_keep:
        if id in nearest_node_cafes:
            nodes_to_keep_id.append(nearest_node_cafes[id])
    #print(len(nodes_to_keep_id))

     # Create a new graph with only the nodes and edges we need - not sure
    # about this
    updated_G = nx.Graph()
    updated_G.add_nodes_from(nodes_to_keep)
    updated_G.add_edges_from([(u, v) for u, v in G.edges() if u in nodes_to_keep and v in nodes_to_keep])
    print(len(updated_G.edges))

    return

def create_nodeid_dict(nodes, nearest_node_cafes):
  num_vertices = len(nodes)

  for i in range(num_vertices):
    nodeid = nodes.iloc[i].name
    idx = i
    nearest_node_cafes[nodeid] = idx

  return nearest_node_cafes

# populates cafe_dict structure
def create_cafe_dict(cafe_dict, fullerton_cafes):
    num_cafes = len(fullerton_cafes)

    for i in range(num_cafes):
        name = fullerton_cafes.iloc[i]['name']
        if not pd.isna(name):  # Ignoring features that do not have a name
            osmid = int(fullerton_cafes.iloc[i].name[1])
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
        if isinstance(coordinates, shapely.geometry.point.Point):
            coordinates = list(coordinates.coords)  # get coordinates Geometry is backwards
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