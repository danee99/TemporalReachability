import multiprocessing
import os
import time
from queue import PriorityQueue
import heapq_max
import numpy as np
import copy
from timeit import default_timer as timer
import intervals as I


class TemporalGraph:
    def __init__(self, nodes, incidence_list):
        self.n = 0
        self.nodes = []
        self.incidence_list = []
        self.outdegree = []
        self.indegree = []
        self.reachabilities = []
        self.deleted_nodes = set()
        self.reachsets = []

    def print_graph(self):
        for node in self.nodes:
            print(str(node) + ": " + str(self.incidence_list[node]) + " " + str(self.reachabilities[node]))

    def import_edgelist(self, file_name):
        with open(os.getcwd() + file_name, "r") as f:
            n = int(f.readline())
            self.n = n
            self.incidence_list = [[] for _ in range(n)]
            self.outdegree = [0 for _ in range(n)]
            self.indegree = [0 for _ in range(n)]
            self.reachabilities = [1 for _ in range(n)]
            self.reachsets = [set() for _ in range(n)]
            for line in f:
                arr = line.split()
                u = int(arr[0])
                v = int(arr[1])
                t = int(arr[2])
                try:
                    l = int(arr[3])
                except IndexError:
                    l = 1
                if u not in self.nodes:
                    self.nodes.append(u)
                if v not in self.nodes:
                    self.nodes.append(v)
                self.outdegree[u] = self.outdegree[u] + 1
                self.indegree[v] = self.indegree[v] + 1
                self.incidence_list[u].append((u, v, t, l))

    def calc_reachabilities(self, a, b):
        # total = 0
        for node in self.nodes:
            reach_set = {node}
            earliest_arrival_time = [np.inf for _ in range(self.n)]
            earliest_arrival_time[node] = 0
            PQ = PriorityQueue()
            PQ.put((earliest_arrival_time[node], node))
            while not PQ.empty():
                (current_arrival_time, current_node) = PQ.get()
                for (u, v, t, l) in self.incidence_list[current_node]:
                    if t < a or t + l > b: continue
                    if t + l < earliest_arrival_time[v] and t >= current_arrival_time:
                        reach_set.add(v)
                        earliest_arrival_time[v] = t + l
                        PQ.put((earliest_arrival_time[v], v))
            self.reachsets[node] = reach_set
            self.reachabilities[node] = len(reach_set)
            # total = total + len(reach_set)
        # return total

    def filter_nodes(self):
        for node in self.nodes:
            if self.outdegree[node] == 0:
                self.deleted_nodes.add(node)
                self.reachsets[node] = set()
        for node in self.nodes:
            self.reachsets[node] - self.deleted_nodes
        for node in self.nodes:
            self.reachabilities[node] = len(self.reachsets[node])
        return sum(self.reachabilities)


    def total_reachability_after(self, a, b):
        self.filter_nodes()
        return sum(self.reachabilities)


if __name__ == '__main__':
    input_graph = '/edge-lists/' + input('Edgeliste eingeben:')
    output_file = input_graph.split(".")[0] + '-Heuristik-Top-' + str(10) + '.txt'
    G = TemporalGraph([], [])
    G.import_edgelist(input_graph)
    G.calc_reachabilities(0, np.inf)
    G.filter_nodes()
    G.print_graph()
    # kCore = G.k_core_decomposition2()
    # for v in G.nodes:
    #     print("Knoten (" + str(v) + ") gehört zum " + str(kCore[v]) + "-Core")
    # example_graph2.txt
    # example_graph1.txt
