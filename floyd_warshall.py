"""
GROUP 1: Anunay Amrit, Angelica Cabato, Pranav Vijay Chand, Riya Chapatwala, Sai Satya Jagannadh Doddipatla, Nhat Ho

Dr. Shah

CPSC 535: Advanced Algorithms (Spring 2024)

"""
# Reference: https://www.programiz.com/dsa/floyd-warshall-algorithm
import numpy as np

def floyd_warshall(graph, index_mapping):
    num_vertices = len(graph.nodes)
    # initialize graph
    dist = np.full((num_vertices, num_vertices), np.inf)
    np.fill_diagonal(dist, 0)

    # print(f"number of nodes {num_vertices}")
    edges_with_attributes = graph.edges(data=True)
    for edge in edges_with_attributes:
        i, j, attributes = edge # i, j are original index
        length = attributes.get('length', np.inf)
        index_mapped_i, index_mapped_j = index_mapping[i], index_mapping[j]
        dist[index_mapped_i, index_mapped_j] = length

    print(f"number of nodes {num_vertices}")
    print("Distance Matrix After:\n", dist)

    # iterate over the graph and update the matrix if new shortest path is found
    for k in range(num_vertices):
        print(f"-----------------------kkkkkkkkkkkkkkkk------------------------: {k}")
        for i in range(num_vertices):
            if np.isinf(dist[i, k]): # reduced calculation
                continue
            for j in range(num_vertices):
                if np.isinf(dist[k, j]): # reduced calculation
                    continue
                new_distance = dist[i, k] + dist[k, j]
                if np.isinf(dist[i, j]): # reduced calculation
                    dist[i, j] = new_distance
                elif new_distance < dist[i, j]:
                    dist[i, j] = new_distance
    return dist    
    