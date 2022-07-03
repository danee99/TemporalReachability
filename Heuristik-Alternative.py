import multiprocessing
import os
import time
from queue import PriorityQueue
import numpy as np


class TemporalGraph:
    def __init__(self):
        self.n = 0
        self.m = 0
        self.graph = {}
        self.change = {}
        self.change_of_deleted_nodes = 0
        self.num_deleted_nodes = 0
        # outgoing edges from id = in self.graph[id][0]
        # outdegree(id) = self.graph[id][1]

    def add_edge(self, u, v, t, l):
        if u not in self.graph:
            self.graph[u] = [(u, v, t, l)]
        else:
            self.graph[u].append((u, v, t, l))
        if v not in self.graph:
            self.graph[v] = []
        self.m += 1

    def print_graph(self):
        print("|V| = " + str(self.n))
        print("|E| = " + str(self.m))
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

    def filter_nodes(self, depth):
        # Problem 1: Erreichbarkeiten der In-Nachbarn der gelöschten Knoten speichern
        # Problem 2: Erreichbarkeiten der gelöschten Knoten speichern
        # Problem 3: Erreichbarkeiten von x fallen bei der Berechnung von R(G-x) weg
        deleted_nodes = []
        for i in range(0, depth):
            for node in self.graph:
                if len(self.graph[node]) == 0:
                    deleted_nodes.append(node)
                    self.num_deleted_nodes += 1
                    if node not in self.change:
                        self.change[node] = 1
                    else:
                        self.change[node] += 1
            for node in self.graph:
                visited = set()
                for (u, v, t, l) in self.graph[node][:]:
                    if v in deleted_nodes:
                        if v not in visited:
                            if node not in self.change:
                                self.change[u] = 0
                            self.change[u] += 1
                        self.graph[u].remove((u, v, t, l))
                        self.m -= 1
                        visited.add(v)
            while deleted_nodes:
                delete_me = deleted_nodes.pop(0)
                self.change_of_deleted_nodes += self.change[delete_me]
                try:
                    del self.graph[delete_me]
                    self.n -= 1
                except KeyError:
                    continue

    def calculate_bounds(self, a, b, x):
        lower_bound = self.change_of_deleted_nodes
        upper_bound = self.change_of_deleted_nodes
        for node in self.graph:
            if node == x:
                continue
            reach_set = {node}
            visited = set()
            earliest_arrival_time = {v: np.inf for v in self.graph}
            earliest_arrival_time[node] = 0
            PQ = PriorityQueue()
            PQ.put((earliest_arrival_time[node], node))
            while not PQ.empty():
                (current_arrival_time, current_node) = PQ.get()
                if current_node not in visited:
                    for (u, v, t, l) in self.graph[current_node]:
                        if u != x and v != x:
                            if t < a or t + l > b: continue
                            if t + l < earliest_arrival_time[v] and t >= current_arrival_time:
                                reach_set.add(v)
                                earliest_arrival_time[v] = t + l
                                PQ.put((earliest_arrival_time[v], v))
                    visited.add(current_node)
            try:
                lower_bound += len(reach_set) + self.change[node]
            except KeyError:
                lower_bound += len(reach_set)
            upper_bound += len(reach_set)+self.num_deleted_nodes
        return x, (lower_bound, upper_bound)

    def heuristik(self, a, b, output_name, depth):
        num_edges = self.m
        num_nodes = self.n
        start_time = time.time()
        self.filter_nodes(depth)
        finish1 = time.time() - start_time
        pool = multiprocessing.Pool(multiprocessing.cpu_count())
        result_objects = [pool.apply_async(self.calculate_bounds, args=(a, b, node)) for node
                          in self.graph]
        ranking = [r.get() for r in result_objects]
        pool.close()
        pool.join()
        finish2 = time.time() - start_time
        with open(os.getcwd() + output_name, 'w') as f:
            ranking.sort(key=lambda tup: tup[1][0])
            f.write(str(ranking) + "\n")
            f.write("mit Tiefe = " + str(depth) + "\n")
            f.write("geloeschte Knotenanzahl = " + str(num_nodes - self.n) + "\n")
            f.write("geloeschte Kanten = " + str(num_edges - self.m) + "\n")
            f.write("--- filter_nodes() finished in %s minutes ---" % (finish1 / 60) + "\n")
            f.write("--- finished in %s seconds ---" % finish2 + "\n")
            f.write("--- finished in %s minutes ---" % (finish2 / 60) + "\n")
            f.write("--- finished in %s hours ---" % (finish2 / 3600))


if __name__ == '__main__':
    input_graph = '/edge-lists/' + input('Edgeliste eingeben:')
    depth = int(input('Tiefe eingeben:'))
    heuristik_output_file = input_graph.split(".")[0] + '-Heuristik' + '.txt'
    ranking_output_file = input_graph.split(".")[0] + '-Rangliste' + '.txt'
    G = TemporalGraph()
    G.import_edgelist(input_graph)
    G.heuristik(0, np.inf, heuristik_output_file, depth)
    # num_edges = G.m
    # G.filter_nodes(depth)
    # print(str(len(G.deleted_nodes))+' Knoten gelöscht')
    # print(str(num_edges-G.m)+' Kanten gelöscht')
    # example_graph2.txt
