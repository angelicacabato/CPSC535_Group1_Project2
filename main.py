"""
GROUP 1: Anunay Amrit, Angelica Cabato, Pranav Vijay Chand, Riya Chapatwala, Sai Satya Jagannadh Doddipatla, Nhat Ho

Project 2 Algorithm Specialists: Angelica Cabato, TBD

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

import numpy as np


def floyd_warshall(graph):
    # citation: https://www.programiz.com/dsa/floyd-warshall-algorithm
    # get unique vertices
    vertices = list(set([edge[0] for edge in graph]))
    num_vertices = len(vertices)
    # print("vertices are: ", vertices)

    # initialize graph
    dist = np.matrix(np.ones((num_vertices, num_vertices)) * np.inf)
    print(dist)

    # update matrix with vertices and edges
    for row in graph:
        u = row[0] - 1  # start_vertex
        v = row[1] - 1  # end_vertex
        weight = row[2]
        dist[u, v] = weight

    print("Distance Matrix Before:\n", dist)

    # iterate over the graph and update the matrix if new shortest path is found
    for k in range(num_vertices):
        for i in range(num_vertices):
            for j in range(num_vertices):
                if dist[i, k] + dist[k, j] < dist[i, j]:
                    dist[i, j] = dist[i, k] + dist[k, j]

    print("Distance Matrix After:\n", dist)

    return dist


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
    floyd_warshall(graph)


if __name__ == "__main__":
    main()
