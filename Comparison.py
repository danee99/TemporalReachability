import os
import scipy.stats as stats
import teneto
from teneto import TemporalNetwork
from teneto import networkmeasures
import matplotlib.pyplot as plt


def import_edgelist(file_name):
    edgelist = []
    with open(os.getcwd() + file_name, "r") as f:
        int(f.readline())
        for line in f:
            arr = line.split()
            u = int(arr[0])
            v = int(arr[1])
            t = int(arr[2])
            try:
                l = int(arr[3])
            except IndexError:
                l = 1
            if (u, v, t, l) not in edgelist:
                edgelist.append([u, v, t, l])
    return edgelist


def remove_node(file_name, node):
    edgelist = []
    with open(os.getcwd() + file_name, "r") as f:
        int(f.readline())
        for line in f:
            arr = line.split()
            u = int(arr[0])
            v = int(arr[1])
            t = int(arr[2])
            try:
                l = int(arr[3])
            except IndexError:
                l = 1
            if (u, v, t, l) not in edgelist and u != node and v != node:
                edgelist.append([u, v, t, l])
    return edgelist


# edges = import_edgelist("/edge-lists/test.txt")
# nlabs = ['0', '1', '2', '3', '4', '5', '6']
# tnet = TemporalNetwork(from_edgelist=edges, nodelabels=nlabs)
# print("Betweeness: " + str(networkmeasures.temporal_betweenness_centrality(tnet, calc='overtime')))
# print("Degree: " + str(
#     networkmeasures.temporal_degree_centrality(tnet, axis=0, calc='overtime', decay=0, ignorediagonal=True)))
# print("Closeness: " + str(networkmeasures.temporal_closeness_centrality(tnet)))
# tnet.plot('slice_plot', cmap='Set2')
# plt.show()

temp_reach = [0.29729729729729726, 0.2432432432432432, 0.3513513513513513, 0.43243243243243246, 0.21621621621621623,
              0.29729729729729726, 0.2432432432432432]
betweeness = [0.01619048, 0.00544218, 0.04571429, 0.05571429, 0.02142857, 0.02258503, 0.01380952]
degreee = [2., 2., 3., 4., 2., 3., 2.]
tau, p_value = stats.kendalltau(temp_reach, degreee)
print(tau)

# 0.6508140266182865 temp reach ves betweeness für test.txt Graph
# 0.7970811413304555 temp reach vs degree für testt.txt graph
