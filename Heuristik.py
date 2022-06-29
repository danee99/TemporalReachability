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
        self.total_reachability = 0
        self.deleted_nodes = {}
        # outdegree(v) = self.nodes[v][0]
        # indegree(v) = self.nodes[v][1]
        # part that is missing = self.nodes[v][2]

    def add_edge(self, u, v, t, l):
        if u in self.graph:
            self.graph[u].append((u, v, t, l))
        else:
            self.graph[u] = [(u, v, t, l)]
        if u in self.nodes:
            self.nodes[u][0] += 1
        else:
            self.nodes[u] = [1, 0, 0]
        if v not in self.graph:
            self.graph[v] = []
        if v in self.nodes:
            self.nodes[v][1] += 1
        else:
            self.nodes[v] = [0, 1, 0]
        self.m += 1

    def print_graph(self):
        print("|V| = " + str(self.n))
        print("|E| = " + str(self.m))
        for v in self.graph:
            print(str(v) + " " + str(self.graph[v]))
            # print(str(v) + " " + str(self.nodes[v]))

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

    def calc_total_reachability(self, a, b):
        for node in self.nodes:
            reach_set = {node}
            # earliest_arrival_time = [np.inf for _ in range(len(self.nodes))]
            earliest_arrival_time = {v: np.inf for v in self.nodes}
            earliest_arrival_time[node] = 0
            PQ = PriorityQueue()
            PQ.put((earliest_arrival_time[node], node))
            while not PQ.empty():
                (current_arrival_time, current_node) = PQ.get()
                for (u, v, t, l) in self.graph[current_node]:
                    if t < a or t + l > b: continue
                    if t + l < earliest_arrival_time[v] and t >= current_arrival_time:
                        reach_set.add(v)
                        earliest_arrival_time[v] = t + l
                        PQ.put((earliest_arrival_time[v], v))
            self.total_reachability += len(reach_set)

    def rank_node(self, x, a, b, before, helper):
        total = 0
        for node in self.nodes:
            if node == x:
                continue
            reach_set = {node}
            visited = set()
            earliest_arrival_time = helper[:]
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
            total += len(reach_set)
        return 1 - (total / before)

    def node_ranking(self, a, b, output_name):
        start_time = time.time()
        helper = [np.inf for _ in range(self.n)]
        self.calc_total_reachability(a, b)
        start_time2 = time.time()
        pool = multiprocessing.Pool(multiprocessing.cpu_count())
        result_objects = [pool.apply_async(self.rank_node, args=(node, a, b, self.total_reachability, helper)) for node
                          in range(0, self.n)]
        ranking = [r.get() for r in result_objects]
        finish2 = time.time() - start_time2
        pool.close()
        pool.join()
        finish = time.time() - start_time
        with open(os.getcwd() + output_name, 'w') as f:
            f.write(str(ranking) + "\n")
            f.write("R(G) = " + str(self.total_reachability) + "\n")
            f.write("--- ranking finished in %s seconds ---" % finish + "\n")
            f.write("--- finished in %s seconds ---" % finish + "\n")
            f.write("--- finished in %s minutes ---" % (finish / 60) + "\n")
            f.write("--- finished in %s hours ---" % (finish / 3600))

    def calculate_bounds(self, a, b, x, helper):
        upper_bound = 0
        lower_bound = 0
        for node in self.nodes:
            if node == x:
                continue
            reach_set = {node}
            visited = set()
            earliest_arrival_time = helper.copy()
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
            lower_bound += len(reach_set) + self.nodes[node][2]
            upper_bound += len(reach_set) + len(self.deleted_nodes)
        part = sum(self.deleted_nodes.values())
        lower_bound += part
        upper_bound += part
        return x, (lower_bound, upper_bound)

    def filter_nodes(self, depth):
        for i in range(0, depth):
            for node in self.nodes:
                if self.nodes[node][0] == 0:
                    if node not in self.deleted_nodes:
                        self.deleted_nodes[node] = 1
                    self.deleted_nodes[node] += self.nodes[node][2]
            for node in self.nodes:
                visited = set()
                for (u, v, t, l) in self.graph[node][:]:
                    if v in self.deleted_nodes:
                        if v not in visited:
                            self.nodes[u][2] += 1
                        self.nodes[u][0] -= 1
                        self.nodes[v][1] -= 1
                        self.graph[u].remove((u, v, t, l))
                        self.m -= 1
                        visited.add(v)
            for node in self.deleted_nodes:
                try:
                    del self.nodes[node]
                    del self.graph[node]
                    self.n -= 1
                except KeyError:
                    continue

    def heuristik(self, a, b, output_name, depth):
        num_edges = self.m
        start_time = time.time()
        self.filter_nodes(depth)
        finish1 = time.time() - start_time
        helper = {v: np.inf for v in self.nodes}
        pool = multiprocessing.Pool(multiprocessing.cpu_count())
        result_objects = [pool.apply_async(self.calculate_bounds, args=(a, b, node, helper))
                          for node in self.nodes]
        ranking = [r.get() for r in result_objects]
        pool.close()
        pool.join()
        finish2 = time.time() - start_time
        with open(os.getcwd() + output_name, 'w') as f:
            ranking.sort(key=lambda tup: tup[1][0])
            f.write(str(ranking) + "\n")
            f.write("mit Tiefe = " + str(depth) + "\n")
            f.write("geloeschte Knotenanzahl = " + str(len(self.deleted_nodes)) + "\n")
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
    G.node_ranking(0, np.inf, ranking_output_file)
    G.heuristik(0, np.inf, heuristik_output_file, depth)

    # num_edges = G.m
    # G.filter_nodes(depth)
    # print(str(len(G.deleted_nodes))+' Knoten gelöscht')
    # print(str(num_edges-G.m)+' Kanten gelöscht')
