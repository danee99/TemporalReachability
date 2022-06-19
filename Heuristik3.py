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

    def add_edge(self, u, v, t, l):
        if u in self.graph:
            self.graph[u].append((u, v, t, l))
        else:
            self.graph[u] = [(u, v, t, l)]

    def remove_node(self, node):
        del self.nodes[node]
        del self.graph[node]
        self.n -= 1

    def print_graph(self):
        print(self.n)
        print(self.nodes)
        print(self.graph)
        for v in self.graph:
            print(str(v) + " " + str(self.graph[v]))
            print(str(v) + " " + str(self.nodes[v]))

    def print_reachable_nodes(self, node):
        print("Knoten " + str(node) + " erreicht die Knoten: " + str(self.nodes[node][0]))

    def outdegree(self, node):
        return self.nodes[node][1]

    def indegree(self, node):
        return self.nodes[node][2]

    def reach_set(self, node):
        return self.nodes[node][0]

    def num_reachable_nodes(self):
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
            self.total_reachability += len(reach_set)
            self.nodes[node][0] = reach_set
            self.nodes[node][3] = len(reach_set)

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
            result += len(reach_set)
            result += self.change_in_reachability[node]
            # self.nodes[node][0] = reach_set
        return result

    def node_ranking(self, a, b):
        ranking = []
        for node in G.nodes:
            ranking.append((node, G.calc_total_reachability_after(0, np.inf, node)))
        ranking.sort(key=lambda tup: tup[1])
        i = 1
        print("        | v | R(G-v)")
        print("--------|---|-------")
        for item in ranking:
            print(str(i) + ".Platz | " + str(item[0]) + " | " + str(item[1]))
            i += 1

    def filter_nodes(self):
        upper_bound = 0
        for node in self.nodes:
            if self.outdegree(node) == 0:
                self.deleted_nodes.add(node)
        for node in self.nodes:
            if node not in self.deleted_nodes:
                self.nodes[node][3] -= len(self.deleted_nodes)
                upper_bound += self.nodes[node][3]
        # upper_bound = upper_bound+len(self.deleted_nodes)*(self.n-len(self.deleted_nodes)+1)
        print(self.deleted_nodes)
        print(upper_bound)

    # O(depth * n * d_max)
    def stubborn(self, depth):
        i = 0
        while i != depth:
            for node in self.nodes:
                if self.outdegree(node) == 0:
                    self.deleted_nodes.add(node)
                    self.nodes[node][0].discard(node)
                    self.nodes[node][3] = 0
            for node in self.nodes:
                for edge in self.graph[node][:]:
                    if edge[1] in self.deleted_nodes:
                        self.change_in_reachability[edge[0]] += 1 + self.change_in_reachability[edge[1]]
                        self.nodes[edge[0]][0].discard(edge[1])
                        self.nodes[edge[0]][1] -= 1
                        self.nodes[edge[1]][2] -= 1
                        self.nodes[edge[0]][3] -= 1
                        self.graph[edge[0]].remove((edge[0], edge[1], edge[2], edge[3]))
            for node in self.deleted_nodes:
                del self.nodes[node]
                del self.graph[node]
                self.n -= 1
            i += 1

    def stubborn_ranking(self, a, b):
        start_time = time.time()
        G.calc_reachabilities(0, np.inf)
        G.stubborn(1)
        finish = time.time() - start_time
        print(finish)
        ranking = []
        for i in self.nodes:
            ranking.append((i, self.calc_total_reachability_after(a, b, i)))
        ranking.sort(key=lambda tup: tup[1])
        print(ranking)

    def util(self, x, a, b, helper):
        if x not in self.nodes:
            return 0
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
            result += len(reach_set) + self.change_in_reachability[node]
        # return 1 - (result / before)
        return result

    def alternative(self, a, b, output_name, depth):
        start_time = time.time()
        G.calc_reachabilities(0, np.inf)
        n = self.n
        # before = self.total_reachability
        G.stubborn(depth)
        helper = {v: np.inf for v in self.nodes}
        pool = multiprocessing.Pool(multiprocessing.cpu_count())
        result_objects = [pool.apply_async(self.util, args=(node, a, b, helper)) for node in
                          range(0, n)]
        ranking = [r.get() for r in result_objects]
        pool.close()
        pool.join()
        finish = time.time() - start_time
        with open(os.getcwd() + output_name, 'w') as f:
            f.write(str(ranking) + "\n")
            f.write(str(self.total_reachability) + "\n")
            f.write("--- finished in %s seconds ---" % finish + "\n")
            f.write("--- finished in %s minutes ---" % (finish / 60) + "\n")
            f.write("--- finished in %s hours ---" % (finish / 3600))


if __name__ == '__main__':
    input_graph = '/edge-lists/' + input('Edgeliste eingeben:')
    depth = int(input('Tiefe eingeben:'))
    output_file = input_graph.split(".")[0] + '-Rangliste3' + '.txt'
    G = TemporalGraph([], [])
    G.import_edgelist(input_graph)
    # start_time = time.time()
    G.alternative(0, np.inf, output_file, depth)
    # finish = time.time() - start_time
    # example_graph1.txt
    # example_graph2.txt
    # g.txt
