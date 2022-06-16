import multiprocessing
import os
import time
from queue import PriorityQueue
import heapq_max
import numpy as np
import copy
from timeit import default_timer as timer

max_heap = []
k = 10


def log_result(result):
    if result[0] != -1:
        if len(max_heap) < k:
            heapq_max.heappush_max(max_heap, (result[0], result[1]))
        if len(max_heap) >= k:
            if result[0] < max_heap[0][0]:
                heapq_max.heappushpop_max(max_heap, (result[0], result[1]))


class TemporalGraph:
    def __init__(self, nodes, incidence_list):
        self.n = 0
        self.nodes = {}
        self.incidence_list = []
        self.deleted_nodes = set()

    # scans the edgelist and creates TemporalGraph object
    def import_edgelist(self, file_name):
        with open(os.getcwd() + file_name, "r") as f:
            self.n = int(f.readline())
            self.incidence_list = [[] for _ in range(self.n)]
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
                    self.nodes[u] = 0
                if v not in self.nodes:
                    self.nodes[v] = 0
                self.nodes[u] += 1
                self.incidence_list[u].append((u, v, t, l))
            self.nodes = {node: degree for node, degree in
                          sorted(self.nodes.items(), key=lambda item: item[1], reverse=True)}

    def print_graph(self):
        for node in self.nodes:
            print(str(node) + ": " + str(self.incidence_list[node]) + str(self.nodes[node]))

    def k_core_decomposition(self, k):
        min_deg = min(self.nodes.values())
        while min_deg < k:
            for v in self.nodes:
                # if v not in self.deleted_nodes:
                if self.nodes[v] < k:
                    self.deleted_nodes.add(v)
            for v in self.nodes:
                # if v not in self.deleted_nodes:
                for edge in self.incidence_list[v]:
                    if edge[1] in self.nodes:
                        if self.nodes[edge[1]] < k:
                            self.incidence_list[v].remove(edge)
                            self.nodes[v] -= 1
            for v in self.deleted_nodes:
                if v in self.nodes:
                    del self.nodes[v]
            try:
                min_deg = min(self.nodes.values())
            except ValueError:
                min_deg = k

    def top_k_util(self, alpha, beta, k, x, helper):
        total = 0
        for node in range(0, self.n):
            if node == x or node in self.deleted_nodes:
                continue
            reach_set = {node}
            earliest_arrival_time = helper.copy()
            earliest_arrival_time[node] = 0
            PQ = PriorityQueue()
            PQ.put((earliest_arrival_time[node], node))
            while not PQ.empty():
                (current_arrival_time, current_node) = PQ.get()
                for (u, v, t, l) in self.incidence_list[current_node]:
                    if u != x and v != x:
                        if t < alpha or t + l > beta:
                            continue
                        if t + l < earliest_arrival_time[v] and t >= current_arrival_time:
                            reach_set.add(v)
                            earliest_arrival_time[v] = t + l
                            PQ.put((earliest_arrival_time[v], v))
            total = total + len(reach_set)
            if max_heap != [] and len(max_heap) >= k:
                if total > max_heap[0][0]:
                    return -1, x
        return total, x

    def top_k_reachability(self, alpha, beta, k, output_name):
        min_deg = min(self.nodes.values())
        self.k_core_decomposition(1)
        start_time = time.time()
        helper = [np.inf for _ in range(self.n)]
        pool = multiprocessing.Pool(multiprocessing.cpu_count())
        for node in self.nodes:
            pool.apply_async(self.top_k_util, args=(alpha, beta, k, node, helper), callback=log_result)
        pool.close()
        pool.join()
        finish = time.time() - start_time
        with open(os.getcwd() + output_name, 'w') as f:
            f.write("--- finished in %s seconds ---" % finish + "\n")
            f.write("--- finished in %s minutes ---" % (finish / 60) + "\n")
            f.write("--- finished in %s hours ---" % (finish / 3600) + "\n")
            f.write(str(max_heap) + "\n")
            f.write(str([element[1] for element in max_heap]) + "\n")
            f.write("geloeschte Knoten Anzahl " + str(len(self.deleted_nodes)) + "\n")
            f.write("Knotenanzahl des Graphen " + str(len(self.nodes)) + "\n")
            f.write("Kantenanzahl des Graphen " + str(len([self.incidence_list[i] for i in self.nodes])) + "\n")


if __name__ == '__main__':
    input_graph = '/edge-lists/' + input('Edgeliste eingeben:')
    output_file = input_graph.split(".")[0] + '-Heuristik2-Top-' + str(k) + '.txt'
    G = TemporalGraph([], [])
    G.import_edgelist(input_graph)
    G.top_k_reachability(0, np.inf, k, output_file)
