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


# TODO - This function is still in progress
def process_map_data():
    ####Open Street Map Code###

    # pull map data of Fullerton, CA and plot it
    place = {"city": "Fullerton", "state": "California", "country": "USA"}
    G = ox.graph_from_place(place, network_type="drive", truncate_by_edge=True)
    #fig, ax = ox.plot_graph(G, figsize=(10, 10), node_size=0, edge_color="y",
                            #edge_linewidth=0.2)

    #Convert graph to GeoDataFrames
    gdf_nodes, gdf_edges = ox.graph_to_gdfs(G)
    #print(gdf_nodes.head().to_string())
    #print(gdf_edges.head().to_string())


    # Example using built it shortest path function
    orig = 20972501
    dest = 67543020
    route = ox.shortest_path(G, orig, dest, weight="length")
    fig, ax = ox.plot_graph_route(G, route, node_size=0)
    plt.show()

    return None