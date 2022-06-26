import multiprocessing
import os
import time
from queue import PriorityQueue
import intervals as I
import numpy as np


class TemporalGraph:
    def __init__(self):
        self.n = 0
        self.before = 0
        self.m = 0
        self.nodes = {}
        self.graph = {}
        self.deleted_nodes = set()
        self.total_reachability = 0
        self.change_in_reachability = {}
        # outdegree(v) = self.nodes[v][0]
        # indegree(v) = self.nodes[v][1]

    def add_edge(self, u, v, t, l):
        if u in self.graph:
            self.graph[u].append((u, v, t, l))
        else:
            self.graph[u] = [(u, v, t, l)]

    def print_graph(self):
        print(self.n)
        for v in self.graph:
            print(str(v) + " " + str(self.graph[v]))
            print(str(v) + " " + str(self.nodes[v]))

    def import_edgelist(self, file_name):
        with open(os.getcwd() + file_name, "r") as f:
            self.n = int(f.readline())
            self.before = self.n
            for line in f:
                arr = line.split()
                u = int(arr[0])
                v = int(arr[1])
                t = int(arr[2])
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
        # self.change_in_reachability = {v: 0 for v in self.nodes}

    def calc_total_reachability_after(self, a, b, x, helper):
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
            lower_bound += len(reach_set)
            upper_bound += len(reach_set) + len(self.deleted_nodes)
        lower_bound += sum(len(value) for key, value in self.change_in_reachability.items()
                           if key != x)
        upper_bound += sum(len(value) for key, value in self.change_in_reachability.items()
                           if key in self.deleted_nodes)
        return x, (lower_bound, upper_bound)

    def quick_node_ranking_test(self, a, b, depth):
        self.filter_nodes(depth)
        file = "/edge-lists/noderankingtest.txt"
        pool = multiprocessing.Pool(multiprocessing.cpu_count())
        result_objects = [pool.apply_async(self.calc_total_reachability_after, args=(0, np.inf, node))
                          for node in self.nodes]
        rankings = [r.get() for r in result_objects]
        rankings.sort(key=lambda tup: tup[:][1].lower)
        print(rankings)
        # example_graph2.txt

    def filter_nodes(self, depth):
        i = 0
        while i != depth:
            deletion = set()
            for node in self.nodes:
                if self.nodes[node][0] == 0:
                    deletion.add(node)
            for node in self.nodes:
                for (u, v, t, l) in self.graph[node][:]:
                    if v in deletion:
                        if u not in self.change_in_reachability:
                            self.change_in_reachability[u] = 0
                        self.change_in_reachability[u] += 1
                        # self.change_in_reachability[u] += 1 + self.change_in_reachability[v]
                        self.nodes[u][0] -= 1
                        self.nodes[v][1] -= 1
                        self.graph[u].remove((u, v, t, l))
                        self.m -= 1
            self.deleted_nodes = self.deleted_nodes | deletion
            for node in self.deleted_nodes:
                try:
                    del self.nodes[node]
                    del self.graph[node]
                    self.n -= 1
                except KeyError:
                    continue
            i += 1

    def filter_nodes2(self, depth):
        for i in range(0, depth):
            for node in self.nodes:
                if self.nodes[node][0] == 0:
                    self.deleted_nodes.add(node)
                    if node not in self.change_in_reachability:
                        self.change_in_reachability[node] = set()
                    self.change_in_reachability[node].add(node)
            for node in self.nodes:
                for (u, v, t, l) in self.graph[node][:]:
                    if v in self.deleted_nodes:
                        if u not in self.change_in_reachability:
                            self.change_in_reachability[u] = set()
                        self.change_in_reachability[u].add(v)
                        self.nodes[u][0] -= 1
                        self.graph[u].remove((u, v, t, l))
                        self.m -= 1
            for node in self.deleted_nodes:
                try:
                    del self.nodes[node]
                    del self.graph[node]
                    self.n -= 1
                except KeyError:
                    continue

    def node_ranking(self, a, b, output_name, depth):
        start_time = time.time()
        G.filter_nodes2(depth)
        finish1 = time.time() - start_time
        helper = {v: np.inf for v in self.nodes}
        pool = multiprocessing.Pool(multiprocessing.cpu_count())
        result_objects = [pool.apply_async(self.calc_total_reachability_after, args=(a, b, node, helper)) for node in
                          self.nodes]
        ranking = [r.get() for r in result_objects]
        pool.close()
        pool.join()
        finish2 = time.time() - start_time
        ranking.sort(key=lambda tup: tup[:][1][0])
        with open(os.getcwd() + output_name, 'w') as f:
            f.write(str(ranking) + "\n")
            f.write("mit Tiefe = " + str(depth) + "\n")
            f.write("--- finished in %s seconds ---" % finish2 + "\n")
            f.write("--- filter_nodes() finished in %s minutes ---" % (finish1 / 60) + "\n")
            f.write("--- finished in %s minutes ---" % (finish2 / 60) + "\n")
            f.write("--- finished in %s hours ---" % (finish2 / 3600))


if __name__ == '__main__':
    input_graph = '/edge-lists/' + input('Edgeliste eingeben:')
    depth = int(input('Tiefe eingeben:'))
    output_file = input_graph.split(".")[0] + '-Heuristik4' + '.txt'
    # test = input_graph.split(".")[0] + '-_TEST' + '.txt'
    G = TemporalGraph()
    G.import_edgelist(input_graph)
    G.node_ranking(0, np.inf, output_file, depth)
