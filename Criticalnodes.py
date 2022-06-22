import multiprocessing
import os
import time
from queue import PriorityQueue

import numpy as np


class TemporalGraph:
    def __init__(self):
        self.n = 0
        self.m = 0
        self.nodes = {}
        self.graph = {}
        self.deleted_nodes = set()
        self.t_max = 0
        # outdegree(v) = self.nodes[v][0]
        # indegree(v) = self.nodes[v][1]

    def add_edge(self, u, v, t, l):
        if u in self.graph:
            self.graph[u].append((u, v, t, l))
        else:
            self.graph[u] = [(u, v, t, l)]

    def print_graph(self):
        print(self.n)
        print(self.m)
        print(self.graph)
        for v in self.graph:
            print(str(v) + " " + str(self.graph[v]))
            print(str(v) + " " + str(self.nodes[v]))

    def import_edgelist(self, file_name):
        with open(os.getcwd() + file_name, "r") as f:
            self.n = int(f.readline())
            for line in f:
                arr = line.split()
                u = int(arr[0])
                v = int(arr[1])
                t = int(arr[2])
                self.t_max = max(t, self.t_max)
                l = int(arr[3])
                self.add_edge(u, v, t, l)
                if u in self.nodes:
                    self.nodes[u][0] += 1
                else:
                    self.nodes[u] = [1, 0]
                if v in self.nodes:
                    self.nodes[v][1] += 1
                else:
                    self.nodes[v] = [0, 1]
                    self.graph[v] = []
                self.m += 1

    def invert_graph(self, file_name):
        G_R = TemporalGraph()
        with open(os.getcwd() + file_name, "r") as f:
            for line in f:
                arr = line.split()
                v = int(arr[0])
                u = int(arr[1])
                t = int(arr[2])
                l = int(arr[3])
                if u in self.graph:
                    self.graph[u].append((u, v, self.t_max - t, l))
                else:
                    self.graph[u] = [(u, v, self.t_max - t, l)]
                if u in self.nodes:
                    self.nodes[u][0] += 1
                else:
                    self.nodes[u] = [1, 0]
                if v in self.nodes:
                    self.nodes[v][1] += 1
                else:
                    self.nodes[v] = [0, 1]
                    self.graph[v] = []
                self.m += 1
        return G_R

    def DFS_util(self, v, visited):
        visited[v] = True
        for i in self.graph[v]:
            if not visited[i]:
                self.DFS_util(i, visited)

    def fill_order(self, v, visited, stack):
        visited[v] = True
        for i in self.graph[v]:
            if not visited[i]:
                self.fill_order(i, visited, stack)
        stack = stack.append(v)

    def get_SCCs(self, edge_list):
        stack = []
        visited = [False] * self.n
        for i in range(self.n):
            if not visited[i]:
                self.fill_order(i, visited, stack)
        gr = self.invert_graph(edge_list)
        visited = [False] * self.n
        while stack:
            i = stack.pop()
            if not visited[i]:
                gr.DFS_util(i, visited)


    def MostCriticalNode(self, edge_list):
        # Annahme (Problem): G ist stark zusammenhängend
        # Falls nicht: Algorithmus auf jeder SCC von G separat ausführen und Knoten v auswählen, der f(G\v) minimiert
        # die maximale Größe eines SCC für temp. Graphen zu berechnen ist NP-schwer

        # 1. Berechne den inversen temporalen Digraphen G^R
        GR = self.invert_graph(edge_list)

        # 2. Wähle einen beliebigen Startknoten s in V

        # 3. Berechne die Dominatorbaume D sowie D^R der flow-Graphen G_s bzw. G_s^R
        # 4. Berechne die Mengen der nichttrivialen Dominatoren N und N^R der flow-Graphen
        # 5. Berechne die loop nesting trees H und H^R
        # 6. cnode = 0, cvalue = f(G), value = 0
        # 7. für jeden starken Artikulationspunkt v von G:
        # 8.    Berechne Konnektivitätswert für v
        # 9.    if cvalue > value then (Der Knoten mit dem kleinsten Wert ist der kritischste Knoten)
        # 10.       cnode = v
        # 11.       cvalue = value
        # 12. return cnode


if __name__ == '__main__':
    input_graph = '/edge-lists/' + input('Edgeliste eingeben:')
    depth = int(input('Tiefe eingeben:'))
    output_file = input_graph.split(".")[0] + '-Rangliste3' + '.txt'
    G = TemporalGraph()
    G.import_edgelist(input_graph)
    G.node_ranking(0, np.inf, output_file, depth)
    # finish = time.time() - start_time
