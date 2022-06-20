import multiprocessing
import os
import time
from queue import PriorityQueue
import heapq_max
import numpy as np
import copy
from timeit import default_timer as timer
import intervals as I

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
        self.nodes = []
        self.incidence_list = []
        self.outdegree = []
        self.indegree = []
        self.deleted_nodes = set()

    def print_graph(self):
        for node in range(0, self.n):
            print(str(node) + ": " + str(self.incidence_list[node]) + str(self.outdegree[node]))

    # scans the edgelist and creates TemporalGraph object
    def import_edgelist(self, file_name):
        with open(os.getcwd() + file_name, "r") as f:
            n = int(f.readline())
            self.n = n
            self.incidence_list = [[] for _ in range(n)]
            self.outdegree = [0 for _ in range(n)]
            self.indegree = [0 for _ in range(n)]
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

    def k_core_decomposition(self, k):
        min_deg = min(self.outdegree)
        while min_deg < k:
            for node in self.nodes:
                if self.outdegree[node] < k:
                    self.nodes.remove(node)
                    self.deleted_nodes.add(node)
            for node in self.nodes:
                for edge in self.incidence_list[node]:
                    if self.outdegree[edge[1]] < k:
                        self.incidence_list[node].remove(edge)
                        self.outdegree[node] -= 1
            try:
                min_deg = min([self.outdegree[x] for x in self.nodes])
            except ValueError:
                min_deg = k

    def filter_outdegree(self, param):
        for node in self.nodes:
            if self.outdegree[node] <= param:
                self.deleted_nodes.add(node)
                self.nodes.remove(node)
        for node in self.nodes:
            for edge in self.incidence_list[node]:
                if self.outdegree[edge[1]] <= param:
                    # self.outdegree[node] -= 1
                    self.incidence_list[node].remove(edge)
        self.print_graph()

    def heuristik(self, a, b):
        solution = None
        # self.k_core_decomposition(1)
        self.filter_outdegree(0)
        helper = [np.inf for _ in range(self.n)]
        for x in self.nodes:
            total = 0
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
                        for (u, v, t, l) in self.incidence_list[current_node]:
                            if u != x and v != x:
                                if t < a or t + l > b: continue
                                if t + l < earliest_arrival_time[v] and t >= current_arrival_time:
                                    reach_set.add(v)
                                    earliest_arrival_time[v] = t + l
                                    PQ.put((earliest_arrival_time[v], v))
                        visited.add(current_node)
                total = total + len(reach_set)
            interval = I.closed(total + len(self.deleted_nodes) + sum([self.indegree[i] for i in self.deleted_nodes]),
                                total + (len(self.deleted_nodes) * (self.n - len(self.deleted_nodes) + 1)))
            if solution is None:
                solution = (x, interval)
                continue
            if interval <= solution[1]:
                solution = (x, interval)
        print(solution)

    # if sol in aktuell --> aktuell ist definitiv besser wenn sol.lower > aktuell.upper. sonst ist sol besser
    # if sol not in aktuell --> if sol <= aktuell --> sol ist definitiv besser
    # if sol not in aktuell --> if sol >= aktuell --> aktuell ist definitiv besser
    # if sol not in aktuell --> if sol.lower < aktuell.lower and sol.upper > aktuell.upper --> aktuell oder sol
    # möglichkeit 1 : Differenz messen

    def top_k_util(self, alpha, beta, k, x, helper):
        total = 0
        for node in range(0, self.n):
            if node == x or node in self.deleted_nodes:
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
                    for (u, v, t, l) in self.incidence_list[current_node]:
                        if u != x and v != x:
                            if t < alpha or t + l > beta:
                                continue
                            if t + l < earliest_arrival_time[v] and t >= current_arrival_time:
                                reach_set.add(v)
                                earliest_arrival_time[v] = t + l
                                PQ.put((earliest_arrival_time[v], v))
                    visited.add(current_node)
            total = total + len(reach_set)
            if max_heap != [] and len(max_heap) >= k:
                if total > max_heap[0][0]:
                    return -1, x
        return total, x

    def top_k_reachability(self, alpha, beta, k, output_name):
        min_deg = min(self.outdegree)
        start_time = time.time()
        self.k_core_decomposition(min_deg + 1)
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
    output_file = input_graph.split(".")[0] + '-Heuristik-Top-' + str(k) + '.txt'
    G = TemporalGraph([], [])
    G.import_edgelist(input_graph)
    G.heuristik(0, np.inf)
    # kCore = G.k_core_decomposition2()
    # for v in G.nodes:
    #     print("Knoten (" + str(v) + ") gehört zum " + str(kCore[v]) + "-Core")
    # example_graph2.txt
    # example_graph1.txt
