import os

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


edges = import_edgelist("/edge-lists/test.txt")
nlabs = ['0', '1', '2', '3', '4', '5', '6']
tnet = TemporalNetwork(from_edgelist=edges, nodelabels=nlabs)
print("Betweeness: "+str(networkmeasures.temporal_betweenness_centrality(tnet, calc='overtime')))
print("Degree: "+str(networkmeasures.temporal_degree_centrality(tnet, axis=0, calc='overtime', decay=0, ignorediagonal=True)))
print("Closeness: "+str(networkmeasures.temporal_closeness_centrality(tnet)))
# tnet.plot('slice_plot', cmap='Set2')
# plt.show()
