import multiprocessing
import os
import time
from queue import PriorityQueue
import numpy as np


class TemporalGraph:
    def __init__(self):
        self.n = 0
        self.m = 0
        self.total_reachability = 0
        self.graph = {}

    def print_graph(self):
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
                if u not in self.graph:
                    self.graph[u] = [[], 0, 0]
                if v not in self.graph:
                    self.graph[v] = [[], 0, 0]
                if v not in [self.graph[u][0][i][1] for i in range(0, len(self.graph[u][0]))]:
                    self.graph[u][1] += 1
                if v not in [self.graph[u][0][i][1] for i in range(0, len(self.graph[u][0]))]:
                    self.graph[v][2] += 1
                self.graph[u][0].append((u, v, t, l))
                self.m += 1

    def filter_nodes(self, depth):
        X = set()
        # change = 0
        change = []
        num_deleted_nodes = 0
        for i in range(0, depth):
            for v in self.graph:
                if self.graph[v][1] == 0:
                    X.add(v)
                    change.append(v)
            for node in self.graph:
                for (u, v, t, l) in self.graph[node][0][:]:
                    if v in X:
                        change.append(u)
                        self.graph[u][0].remove((u, v, t, l))
                        self.graph[u][1] -= 1
                        self.m -= 1
            num_deleted_nodes += len(X)
            while X:
                v = X.pop()
                try:
                    del self.graph[v]
                    self.n -= 1
                except KeyError:
                    continue
        return change, num_deleted_nodes

    def calculate_bounds(self, a, b, x, helper, change, num_deleted_nodes):
        lower_bound = 0
        upper_bound = 0
        for node in self.graph:
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
                    for (u, v, t, l) in self.graph[current_node][0]:
                        if u != x and v != x:
                            if t < a or t + l > b: continue
                            if t + l < earliest_arrival_time[v] and t >= current_arrival_time:
                                reach_set.add(v)
                                earliest_arrival_time[v] = t + l
                                PQ.put((earliest_arrival_time[v], v))
                    visited.add(current_node)
            lower_bound += len(reach_set)
            upper_bound += len(reach_set) + num_deleted_nodes
        part = len([v for v in change if v != x])
        lower_bound += part
        upper_bound += part
        return x, (lower_bound, upper_bound)

    def heuristik(self, a, b, output_name, depth):
        num_edges = self.m
        start_time = time.time()
        change, num_deleted_nodes = self.filter_nodes(depth)
        finish1 = time.time() - start_time
        helper = {v: np.inf for v in self.graph}
        pool = multiprocessing.Pool(multiprocessing.cpu_count())
        result_objects = [pool.apply_async(self.calculate_bounds, args=(a, b, node, helper, change, num_deleted_nodes))
                          for node in self.graph]
        ranking = [r.get() for r in result_objects]
        pool.close()
        pool.join()
        finish2 = time.time() - start_time
        with open(os.getcwd() + output_name, 'w') as f:
            ranking.sort(key=lambda tup: tup[1][0])
            f.write(str(ranking) + "\n")
            f.write("mit Tiefe = " + str(depth) + "\n")
            f.write("geloeschte Kanten = " + str(num_edges - self.m) + "\n")
            f.write("--- filter_nodes() finished in %s minutes ---" % (finish1 / 60) + "\n")
            f.write("--- finished in %s seconds ---" % finish2 + "\n")
            f.write("--- finished in %s minutes ---" % (finish2 / 60) + "\n")
            f.write("--- finished in %s hours ---" % (finish2 / 3600))

    def calc_total_reachability(self, a, b):
        for node in self.graph:
            reach_set = {node}
            earliest_arrival_time = [np.inf for _ in range(self.n)]
            earliest_arrival_time[node] = 0
            PQ = PriorityQueue()
            PQ.put((earliest_arrival_time[node], node))
            while not PQ.empty():
                (current_arrival_time, current_node) = PQ.get()
                for (u, v, t, l) in self.graph[current_node][0]:
                    if t < a or t + l > b: continue
                    if t + l < earliest_arrival_time[v] and t >= current_arrival_time:
                        reach_set.add(v)
                        earliest_arrival_time[v] = t + l
                        PQ.put((earliest_arrival_time[v], v))
            self.total_reachability += len(reach_set)

    def rank_node(self, x, a, b, before, helper):
        total = 0
        for node in self.graph:
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
                    for (u, v, t, l) in self.graph[current_node][0]:
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
        pool = multiprocessing.Pool(multiprocessing.cpu_count())
        result_objects = [pool.apply_async(self.rank_node, args=(node, a, b, self.total_reachability, helper)) for node
                          in range(0, self.n)]
        ranking = [r.get() for r in result_objects]
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


if __name__ == '__main__':
    input_graph = '/edge-lists/' + input('Edgeliste eingeben:')
    depth = int(input('Tiefe eingeben:'))
    heuristik = input_graph.split(".")[0] + '-Heuristik' + '.txt'
    ranking = input_graph.split(".")[0] + '-Rangliste' + '.txt'
    G = TemporalGraph()
    G.import_edgelist(input_graph)
    G.print_graph()
    # G.node_ranking(0, np.inf, ranking)
    # G.heuristik(0, np.inf, heuristik, depth)


