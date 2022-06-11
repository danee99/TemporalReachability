import multiprocessing
import os
import time
from queue import PriorityQueue
import heapq_max
import numpy as np
import copy
import interval

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
                self.incidence_list[u].append((u, v, t, l))

    def k_core_decomposition(self, k):
        for node in range(0, self.n):
            if self.outdegree[node] == 0:
                self.deleted_nodes.add(node)
                continue
            self.incidence_list[node] = [(u, v, t, l) for (u, v, t, l) in self.incidence_list[node] if
                                         self.outdegree[u] > k and self.outdegree[v] > k]

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
        start_time = time.time()
        helper = [np.inf for _ in range(self.n)]
        pool = multiprocessing.Pool(multiprocessing.cpu_count())
        for node in range(0, self.n):
            if node not in self.deleted_nodes:
                pool.apply_async(self.top_k_util, args=(alpha, beta, k, node, helper), callback=log_result)
        pool.close()
        pool.join()
        finish = time.time() - start_time
        with open(os.getcwd() + output_name, 'w') as f:
            f.write("--- finished in %s seconds ---" % finish + "\n")
            f.write(str(max_heap) + "\n")
            # f.write("Anzahl Knoten mit outgrad = 0: " + str(len(self.deleted_nodes)))


if __name__ == '__main__':
    input_graph = '/edge-lists/' + input('Edgeliste eingeben:')
    output_file = input_graph.split(".")[0] + '-Heuristik-Top-' + str(k) + '.txt'
    G = TemporalGraph([], [])
    G.import_edgelist(input_graph)
    # G.k_core_decomposition(2)
    # G.print_graph()
    G.k_core_decomposition(2)
    G.top_k_reachability(0, np.inf, k, output_file)
    # DATASETS:
    # wiki_talk_nl.txt                      |  |V| = 225.749 | |E| = 1.554.698
    # wikipediasg.txt                       |  |V| = 208.142 | |E| = 810.702
    # facebook.txt                          |  |V| = 63.731  | |E| = 817.035
    # infectious.txt                        |  |V| = 10.972  | |E| = 415.912    234.7 min
    # ia-contacts_dublin.txt                |  |V| = 10.972  | |E| = 415.912
    # copresence-InVS15.txt                 |  |V| = 219     | |E| = 1.283.194
    # copresence-InVS13.txt                 |  |V| = 95      | |E| = 394.247    0.772 min
    # ia-reality-call.txt                   |  |V| = 6.809   | |E| = 52.050
    # ht09_contact_list.txt                 |  |V| = 5.351   | |E| = 20.817     2.727 min
    # twitter.txt                           |  |V| = 4.605   | |E| = 23.736     352.0 min
    # fb-messages.txt                       |  |V| = 1.899   | |E| = 61.734
    # email-dnc.txt                         |  |V| = 1.891   | |E| = 39.264     67.23 min
    # tij_SFHH.txt                          |  |V| = 403     | |E| = 70.261
    # fb-forum.txt                          |  |V| = 899     | |E| = 33.720     9.164 min
    # reptilia-tortoise-network-fi.txt      |  |V| = 787     | |E| = 1.713      0.053 min
    # aves-weaver-social.txt                |  |V| = 445     | |E| = 1.426      0.022 min
    # example_graph1.txt                    |  |V| = 7       | |E| = 18         0.005 min
    # example_graph2.txt                    |  |V| = 7       | |E| = 9          0.005 min
