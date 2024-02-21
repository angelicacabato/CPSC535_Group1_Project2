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
from process_map_data import process_map_data


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
    #floyd_warshall(graph)
    process_map_data()


if __name__ == "__main__":
    main()

