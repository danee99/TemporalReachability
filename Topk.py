import heapq
import os
import time
from queue import PriorityQueue
import heapq_max
import numpy as np

result_list = []


def log_result(result):
    heapq.heappush(result_list, result)


class TemporalGraph:
    def __init__(self, nodes, incidence_list):
        self.n = 0
        self.nodes = []
        self.incidence_list = []

    # scans the edgelist and adds all nodes and edges to the Graph
    # Graph is created in O(m) because all edges are iterated through
    def import_edgelist(self, file_name):
        with open(os.getcwd() + file_name, "r") as f:
            n = int(f.readline())
            self.n = n
            self.incidence_list = [[] for _ in range(n)]
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
                self.incidence_list[u].append((u, v, t, l))

    def util(self, x, alpha, beta, k, max_heap, helper):
        total = 0
        for node in range(0, self.n):
            if node == x:
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
                    return
        if len(max_heap) < k:
            heapq_max.heappush_max(max_heap, (total, x))
        else:
            if total < max_heap[0][0]:
                heapq_max.heappushpop_max(max_heap, (total, x))

    def top_k_agorithm(self, alpha, beta, k):
        start_time = time.time()
        helper = [np.inf for _ in range(self.n)]
        max_heap = []
        for x in range(0, self.n):
            self.util(x, alpha, beta, k, max_heap, helper)
        finish = time.time() - start_time
        print(max_heap, finish)

    def attempt(self, k):
        helper = [np.inf for _ in range(self.n)]
        label_list = []
        F = {}
        T = {}
        for j in range(0, self.n):
            label = (0, j)
            PQ = PriorityQueue()
            PQ.put(label)
            d = helper.copy()
            T[j] = [j]
            F[j] = []
            Pie = [[] for _ in range(self.n)]
            d[j] = 0
            i = 1
            while not PQ.empty():
                l = PQ.get()
                v = l[1]
                if v in T[j] and v not in F[j]:
                    d[v] = l[0]
                    T[j].remove(v)
                    F[j].append(v)
                for (v, w, t, l) in self.incidence_list[v]:
                    if l[0] > t+l:
                        label2 = (t+l, v)
                    PQ.put(label2)
                    if w not in F[j]:
                        T[j].append(w)

if __name__ == '__main__':
    input_graph = input('Edgeliste eingeben: ')
    k = int(input('k eingeben: '))
    output_file = input_graph.split(".")[0] + '-DIJKSTRA-' + str(k) + '.txt'
    G = TemporalGraph([], [])
    G.import_edgelist(input_graph)
    G.top_k_agorithm(0, np.inf, k)
    # DATASETS:
    # /edge-lists/wiki_talk_nl.txt          |  |V| = 225.749 | |E| = 1.554.698
    # /edge-lists/wikipediasg.txt           |  |V| = 208.142 | |E| = 810.702
    # /edge-lists/facebook.txt              |  |V| = 63.731  | |E| = 817.035
    # /edge-lists/infectious.txt            |  |V| = 10.972  | |E| = 415.912
    # /edge-lists/ht09_contact_list.txt     |  |V| = 5.351   | |E| = 20.817
    # /edge-lists/tij_SFHH.txt              |  |V| = 3.906   | |E| = 70.261
    # /edge-lists/twitter.txt               |  |V| = 4.605   | |E| = 23.736
    # /edge-lists/email-dnc.txt             |  |V| = 1.891   | |E| = 39.264
    # /edge-lists/aves-weaver-social.txt    |  |V| = 445     | |E| = 1.426
    # /edge-lists/example_graph1.txt        |  |V| = 7       | |E| = 18
    # /edge-lists/example_graph2.txt        |  |V| = 7       | |E| = 9
