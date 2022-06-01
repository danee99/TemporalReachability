import heapq
import multiprocessing
import os
import time
from queue import PriorityQueue
import heapq_max
import numpy as np
from multiprocessing.pool import ThreadPool

max_heap = []
k = 1


def log_result(result):
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

    # scans the edgelist and creates TemporalGraph object
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

    def innen(self, alpha, beta, k, x, helper):
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
                    return np.inf, x
        return total, x

    def aussen(self, alpha, beta, k, output_name):
        start_time = time.time()
        helper = [np.inf for _ in range(self.n)]
        pool = multiprocessing.Pool(multiprocessing.cpu_count())
        for node in range(0, self.n):
            pool.apply_async(self.innen, args=(alpha, beta, k, node, helper), callback=log_result)
        pool.close()
        pool.join()
        finish = time.time() - start_time
        with open(os.getcwd() + output_name, 'w') as f:
            f.write("--- finished in %s seconds ---" % finish + "\n")
            f.write(str(max_heap))


if __name__ == '__main__':
    input_graph = '/edge-lists/aves-weaver-social.txt'
    output_file = input_graph.split(".")[0] + '-Top' + str(k) + '.txt'
    G = TemporalGraph([], [])
    G.import_edgelist(input_graph)
    G.aussen(0, np.inf, k, output_file)
    # DATASETS:
    # /edge-lists/wiki_talk_nl.txt          |  |V| = 225.749 | |E| = 1.554.698
    # /edge-lists/wikipediasg.txt           |  |V| = 208.142 | |E| = 810.702
    # /edge-lists/facebook.txt              |  |V| = 63.731  | |E| = 817.035
    # /edge-lists/infectious.txt            |  |V| = 10.972  | |E| = 415.912    234.7 min
    # /edge-lists/ia-contacts_dublin.txt    |  |V| = 10.972  | |E| = 415.912
    # /edge-lists/copresence-InVS13.txt     |  |V| = 95      | |E| = 394.247
    # /edge-lists/ia-reality-call.txt       |  |V| = 6.809   | |E| = 52.050
    # /edge-lists/ht09_contact_list.txt     |  |V| = 5.351   | |E| = 20.817     2.727 min
    # /edge-lists/twitter.txt               |  |V| = 4.605   | |E| = 23.736     352.0 min
    # /edge-lists/tij_SFHH.txt              |  |V| = 3.906   | |E| = 70.261     2.870 min
    # /edge-lists/fb-messages.txt           |  |V| = 1.899   | |E| = 61.734
    # /edge-lists/email-dnc.txt             |  |V| = 1.891   | |E| = 39.264     67.23 min
    # /edge-lists/fb-forum.txt              |  |V| = 899     | |E| = 33.720
    # reptilia-tortoise-network-fi.txt      |  |V| = 787     | |E| = 1.713
    # /edge-lists/aves-weaver-social.txt    |  |V| = 445     | |E| = 1.426      0.022 min
    # /edge-lists/example_graph1.txt        |  |V| = 7       | |E| = 18         0.005 min
    # /edge-lists/example_graph2.txt        |  |V| = 7       | |E| = 9          0.005 min
