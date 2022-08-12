import os
import numpy as np
from matplotlib import pyplot as plt
import networkx as nx

path = os.path.join(os.getcwd(), os.pardir) + "\\edge-lists\\"


# print(plt.style.available)
# plt.style.use('bmh')
# nodes_x_val = [445, 1891, 4605, 3906, 5351, 10972]
# edges_x_val = [1426, 39264, 23736, 70261, 20817, 415912]
# y_val = [0, 67, 402, 2, 3, 235]
# # in minutes
# plt.plot(edges_x_val, y_val, 'o')
# plt.xlabel("Anzahl Kanten")
# plt.ylabel("Laufzeit")
# plt.title("Abhängigkeit von Knotenanzahl")
# plt.grid(True)
# plt.tight_layout()
# plt.show()


# def draw_graph(file_name):
#     G = nx.Graph()
#     file = path + file_name
#     with open(file) as fp:
#         nothing_important = int(fp.readline())
#         for line in fp:
#             arr = line.split()
#             u = arr[0]
#             v = arr[1]
#             t = arr[2]
#             G.add_edge(int(u), int(v), weight=t)
#     pos = nx.spring_layout(G)
#     weights = nx.get_edge_attributes(G, "weight")
#     nx.draw_networkx(G, pos, with_labels=True)
#     nx.draw_networkx_edge_labels(G, pos, edge_labels=weights)
#     plt.show()
#
#
# draw_graph("example_graph3.txt")
