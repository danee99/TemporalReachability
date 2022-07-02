import os
from queue import PriorityQueue
import numpy as np


class TemporalGraph:
    def __init__(self):
        self.n = 0
        self.m = 0
        self.graph = {}
        self.total_reachability = 0

    def add_edge(self, u, v, t, l):
        if u not in self.graph:
            #
            self.graph[u] = [[(u, v, t, l)], set()]
        else:
            #
            self.graph[u][0].append((u, v, t, l))
        if v not in self.graph:
            #
            self.graph[v] = [[], set()]
        #
        self.graph[u][1].add(v)
        #
        self.graph[v][1].add(u)
        self.m += 1

    def print_graph(self):
        print("|V| = " + str(self.n) + " |E| = " + str(self.m))
        for v in self.graph:
            print(str(v) + " " + str(self.graph[v]))

    def import_edgelist(self, file_name):
        with open(os.getcwd() + file_name, "r") as f:
            self.n = int(f.readline())
            for line in f:
                arr = line.split()
                u = int(arr[0])
                v = int(arr[1])
                t = int(arr[2])
                l = int(arr[3])
                self.add_edge(u, v, t, l)

    def k_neighborhood(self, node, k):
        visited = set()
        queue = [node, -1]
        i = 0
        while queue:
            current_node = queue.pop(0)
            if current_node == -1:
                i += 1
                queue.append(-1)
                if i == k:
                    break
                else:
                    continue
            else:
                #
                for neighbour in self.graph[current_node][1]:
                    if neighbour not in visited:
                        visited.add(neighbour)
                        queue.append(neighbour)
        return visited

    def total_reachability_after(self, deleted_node, a, b, k):
        total = 0
        k_neighbours = self.k_neighborhood(deleted_node, k)
        for node in k_neighbours:
            if node == deleted_node:
                continue
            reach_set = {node}
            visited = set()
            earliest_arrival_time = {c: np.inf for c in k_neighbours}
            earliest_arrival_time[node] = 0
            PQ = PriorityQueue()
            PQ.put((earliest_arrival_time[node], node))
            while not PQ.empty():
                (current_arrival_time, current_node) = PQ.get()
                if current_node not in visited:
                    #
                    for (u, v, t, l) in self.graph[current_node][0]:
                        if u in k_neighbours and v in k_neighbours:
                            if v != deleted_node and u != deleted_node:
                                if t < a or t + l > b: continue
                                if t + l < earliest_arrival_time[v] and t >= current_arrival_time:
                                    reach_set.add(v)
                                    earliest_arrival_time[v] = t + l
                                    PQ.put((earliest_arrival_time[v], v))
                    visited.add(current_node)
            total += len(reach_set)
        return total


if __name__ == '__main__':
    input_graph = '/edge-lists/' + input('Edgeliste eingeben:')
    output_file = input_graph.split(".")[0] + 'k-Nachbarschaft-Ranking' + '.txt'
    G = TemporalGraph()
    G.import_edgelist(input_graph)
    G.print_graph()
    for v in G.graph:
        print(str(v) + ': R(G-v) = ' + str(G.total_reachability_after(v, 0, 99, 2)))
    # num_edges = G.m
    # G.filter_nodes(depth)
    # print(str(len(G.deleted_nodes))+' Knoten gelöscht')
    # print(str(num_edges-G.m)+' Kanten gelöscht')
    # example_graph1.txt
    # example_graph2.txt
