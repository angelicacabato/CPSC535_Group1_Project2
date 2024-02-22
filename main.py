"""
GROUP 1: Anunay Amrit, Angelica Cabato, Pranav Vijay Chand, Riya Chapatwala, Sai Satya Jagannadh Doddipatla, Nhat Ho

Dr. Shah

CPSC 535: Advanced Algorithms (Spring 2024)

"""

"""
sample graph before algo

    1 2 3 4
1 [ 0 3 inf 5 ]
2 [ 2 0 inf 4 ]
3 [ inf 1 0 inf ]
4 [ inf inf 2 0 ]

sample graph after algo

    1 2 3 4
1 [ 0 3 7 5 ]
2 [ 2 0 6 4 ]
3 [ 3 1 0 5 ]
4 [ 5 3 2 0 ]

"""

# importing other python files for data process and algorithm implementation
from floyd_warshall import floyd_warshall
from process_map_data import (buildmap, get_shortest_path,
                              get_shortest_path_builtin, process_map_data,
                              updateDictforBlockages, simulate_blockages,
                              draw_updated_path, index_mapping)


def main():
    # format is [start, end, weight]
    graph = [[1, 1, 0],
             [1, 2, 3],
             [1, 4, 5],
             [2, 1, 2],
             [2, 2, 0],
             [2, 4, 4],
             [3, 2, 1],
             [3, 3, 0],
             [4, 3, 2],
             [4, 4, 0]
             ]
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
    process_map_data()
    source_osm_id = 4704306820  # Start node OSM ID
    dest_osm_id = 1853024624  # End node OSM ID
    blockages = [(source_osm_id, dest_osm_id)]  # Replace with actual osm IDs
    simulate_blockages(blockages, index_mapping)
    start_osm_id = 122562954 # Start node OSM ID
    end_osm_id = 8816967697 # End node OSM ID
    draw_updated_path(G, start_osm_id, end_osm_id, index_mapping, next)

if __name__ == "__main__":
    main()

