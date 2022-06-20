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
        self.nodes = {}
        self.graph = {}
        self.deleted_nodes = set()
        self.total_reachability = 0
        self.change_in_reachability = {}
        # set-of-reachable-nodes(v) = self.nodes[node][0]
        # outdegree(v) = self.nodes[v][1]
        # indegree(v) = self.nodes[v][2]

    def add_edge(self, u, v, t, l):
        if u in self.graph:
            self.graph[u].append((u, v, t, l))
        else:
            self.graph[u] = [(u, v, t, l)]

    def print_graph(self):
        print(self.n)
        print(self.nodes)
        print(self.graph)
        for v in self.graph:
            print(str(v) + " " + str(self.graph[v]))
            print(str(v) + " " + str(self.nodes[v]))

    def print_reachable_nodes(self):
        for node in self.nodes:
            print("Knoten " + str(node) + " erreicht die Knoten: " + str(self.nodes[node][0]))

    def print_num_reachable_nodes(self):
        for node in self.nodes:
            print("Knoten " + str(node) + " erreicht " + str(len(self.nodes[node][0])) + " Knoten")

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
                if u in self.nodes:
                    self.nodes[u][1] += 1
                else:
                    self.nodes[u] = [set(), 1, 0, 0]
                if v in self.nodes:
                    self.nodes[v][2] += 1
                else:
                    self.nodes[v] = [set(), 0, 1, 0]
                    self.graph[v] = []
        self.change_in_reachability = {v: 0 for v in self.nodes}

    def calc_reachabilities(self, a, b):
        for node in self.nodes:
            reach_set = {node}
            earliest_arrival_time = [np.inf for _ in range(len(self.nodes))]
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
            self.total_reachability += len(reach_set) + self.change_in_reachability[node]
            self.nodes[node][0] = reach_set
            self.nodes[node][3] = len(reach_set)
        self.total_reachability += len(self.deleted_nodes)

    def calc_total_reachability_after(self, a, b, x):
        result = 0
        for node in self.nodes:
            if node == x:
                continue
            reach_set = {node}
            visited = set()
            earliest_arrival_time = {v: np.inf for v in self.nodes}
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
            result += len(reach_set) + self.change_in_reachability[node]
            self.nodes[node][0] = reach_set
            self.nodes[node][3] = len(reach_set)
        return result + len(self.deleted_nodes)

    def quick_node_ranking_test(self, a, b):
        pool = multiprocessing.Pool(multiprocessing.cpu_count())
        result_objects = [pool.apply_async(self.calc_total_reachability_after, args=(0, np.inf, node))
                          for node in range(0, self.n)]
        rankings = [r.get() for r in result_objects]
        result = list(zip([v for v in range(0, self.n)], rankings))
        pool.close()
        pool.join()
        result.sort(key=lambda tup: tup[1])
        i = 1
        print("        | v | R(G-v)")
        print("--------|---|-------")
        for item in result:
            print(str(i) + ".Platz | " + str(item[0]) + " | " + str(item[1]))
            i += 1

    def filter_nodes(self, depth):
        i = 0
        while i != depth:
            for node in self.nodes:
                if self.nodes[node][1] == 0:
                    self.deleted_nodes.add(node)
                    self.nodes[node][0].discard(node)
                    self.nodes[node][3] = 0
            for node in self.nodes:
                for (u, v, t, l) in self.graph[node][:]:
                    if v in self.deleted_nodes:
                        self.change_in_reachability[u] += 1 + self.change_in_reachability[v]
                        # self.nodes[u][0].discard(v)
                        # self.nodes[u][3] -= 1
                        self.nodes[u][1] -= 1
                        self.nodes[v][2] -= 1
                        self.graph[u].remove((u, v, t, l))
            for node in self.deleted_nodes:
                try:
                    del self.nodes[node]
                    del self.graph[node]
                    self.n -= 1
                except KeyError:
                    continue
            i += 1
        # print(self.change_in_reachability)

    def util(self, x, a, b, helper):
        result = 0
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
            # result += len(reach_set) + self.change_in_reachability[node]
            result += len(reach_set) + self.change_in_reachability[node]
        return result + len(self.deleted_nodes)

    def node_ranking(self, a, b, output_name, depth):
        start_time = time.time()
        G.filter_nodes(depth)
        helper = {v: np.inf for v in self.nodes}
        pool = multiprocessing.Pool(multiprocessing.cpu_count())
        result_objects = [pool.apply_async(self.util, args=(node, a, b, helper)) for node in
                          self.nodes]
        ranking = [r.get() for r in result_objects]
        pool.close()
        pool.join()
        finish = time.time() - start_time
        with open(os.getcwd() + output_name, 'w') as f:
            f.write(str(ranking) + "\n")
            f.write("R(G) = " + str(self.total_reachability) + "\n")
            f.write("--- finished in %s seconds ---" % finish + "\n")
            f.write("--- finished in %s minutes ---" % (finish / 60) + "\n")
            f.write("--- finished in %s hours ---" % (finish / 3600))


if __name__ == '__main__':
    input_graph = '/edge-lists/' + input('Edgeliste eingeben:')
    depth = int(input('Tiefe eingeben:'))
    output_file = input_graph.split(".")[0] + '-Rangliste3' + '.txt'
    G = TemporalGraph([], [])
    G.import_edgelist(input_graph)
    G.node_ranking(0, np.inf, output_file, depth)
    # start_time = time.time()
    # finish = time.time() - start_time
    # example_graph1.txt
    # example_graph2.txt
    # g.txt
