"""
GROUP 1: Anunay Amrit, Angelica Cabato, Pranav Vijay Chand, Riya Chapatwala, Sai Satya Jagannadh Doddipatla, Nhat Ho

Dr. Shah

CPSC 535: Advanced Algorithms (Spring 2024)

"""
# importing other python files for data process and algorithm implementation
import networkx as nx
import osmnx as ox
import matplotlib.pyplot as plt
from floyd_warshall import floyd_warshall
from process_map_data import (buildmap, get_shortest_path,
                              get_shortest_path_builtin, process_map_data,
                              updateDictforBlockages, simulate_blockages,
                              implement_blockage)

name_to_node_dict = {
    "Pilgrim's Coffee Shop": 4704306820,
    "Santa Fe Express Cafe": 1391863431,
    "Jay's Coffee Waffles & More": 122562954,
    "Kawaii Boba": 2243492748,
    "Starbucks": 2243492752,
    "Intentional Coffee": 67543057,
    "Starbucks": 8816967697,
    "McClain's Coffeehouse": 122836756,
    "Library Cafe": 5197254171,
    "Philz Coffee": 122757283,
    "The Gastronome": 414550180,
    "Starbucks": 3583764518,
    "Starbucks": 1931779371,
    "Max Bloom's Cafe Noir": 122925745,
    "Sharetea": 4083327025,
    "Starbucks": 2243418547,
    "The Coffee Bean & Tea Leaf": 122817213,
    "Starbucks": 2574034240,
    "Donut Star": 122628045,
    "525 Coffee Co": 122731859,
    "Veronese Gallery and Cafe": 122628569,
    "Coffee Code": 122868068,
    "The Smoking Tiger Coffee and Bread": 2243433066,
    "Starbucks": 67543020,
    "Starbucks": 1853024624,
    "Made Coffee": 2325177846,
    "Eggspresso": 122900858,
    "Dripp": 122757243,
    "The Stinger Cafe": 122728319,
}

def main():
    """
    #floyd_warshall(graph)
    process_map_data()
    #get_shortest_path_builtin(4704306820, 1853024624)
    get_shortest_path(4704306820, 1853024624)

    blockages = [(122562954, 8816967697)]
    updateDictforBlockages(blockages)
    get_shortest_path(4704306820, 1853024624)
    # buildmap()
    """
    G = process_map_data()  # processes the Fullerton's map data

    start_user_input = "Pilgrim's Coffee Shop"  #4704306820,
    end_user_input = "Starbucks"    #1853024624

    # Testing different input
    #start_user_input = "Kawaii Boba" # 2243492748
    #end_user_input = "Sharetea" # 4083327025

    source_osm_id = name_to_node_dict.get(start_user_input) # Start node OSM ID coverted from input
    dest_osm_id = name_to_node_dict.get(end_user_input)  # End node OSM ID coverted from input

    # Test name to node matching
    print(f"{start_user_input}'s node ID is {source_osm_id}")
    print(f"{end_user_input}'s node ID is {dest_osm_id}")

    cur_shortest_path = get_shortest_path(source_osm_id, dest_osm_id)
    print(f"The route of the shortest path is {cur_shortest_path}")

    # visualize cur_shortest_path
    fig, ax = ox.plot_graph_route(G, cur_shortest_path, route_color='b',
                                  route_linewidth=6, node_size=0)

    # If button "Report blockage on route, give new route" is pushed,
    # run blockage function
    blockage_value = True  # based on if user presses the button

    updated_path_after_blockage = None
    if blockage_value:
        updated_path_after_blockage = implement_blockage(source_osm_id,
                                                         dest_osm_id,
                                                         cur_shortest_path)
        if updated_path_after_blockage == None:
            print("No possible path between locations due to blockage.")
        else:
            print(f"Updated route after blockage is"
                  f" {updated_path_after_blockage}")
            # Visualize new shortest path after blockage
            fig, ax = ox.plot_graph_route(G, updated_path_after_blockage,
                                          route_color='r', route_linewidth=6,
                                          node_size=0)

if __name__ == "__main__":
    main()
