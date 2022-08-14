import multiprocessing
import os
import time
from queue import PriorityQueue
import heapq_max
import heapq
import numpy as np

max_heap = []
k = 10
# path = os.path.join(os.getcwd(), os.pardir) + "\\edge-lists\\"
path = "/home/stud/degenste/BA/TemporalReachability/edge-lists/"


def log_result(result):
    if result[0] != -1:
        if len(max_heap) < k:
            heapq_max.heappush_max(max_heap, (result[0], result[1]))
        if len(max_heap) >= k:
            if result[0] < max_heap[0][0]:
                heapq_max.heappushpop_max(max_heap, (result[0], result[1]))


class TemporalGraph:
    def __init__(self):
        self.n = 0
        self.nodes = set()
        self.incidence_list = []

    def import_edgelist(self, file_name):
        with open(path + file_name, "r") as f:
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
                self.nodes.add(u)
                self.nodes.add(v)
                self.incidence_list[u].append((u, v, t, l))

    def import_undirected_edgelist(self, file_name):
        with open(path + file_name, "r") as f:
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
                self.nodes.add(u)
                self.nodes.add(v)
                self.incidence_list[u].append((u, v, t, l))
                self.incidence_list[v].append((v, u, t, l))

    def top_k_util(self, x, alpha, beta, helper, loop_counter):
        total = 0
        for node in self.nodes:
            if node == x:
                continue
            loop_counter += 1
            visited = set()
            earliest_arrival_time = helper.copy()
            earliest_arrival_time[node] = alpha
            PQ = []
            heapq.heappush(PQ, (0, node))
            while PQ:
                (current_arrival_time, current_node) = heapq.heappop(PQ)
                if current_node != x:
                    visited.add(current_node)
                for (u, v, t, l) in self.incidence_list[current_node]:
                    if u != x and v != x and v not in visited:
                        if t < alpha or t + l > beta: continue
                        if t + l < earliest_arrival_time[v] and t >= current_arrival_time:
                            earliest_arrival_time[v] = t + l
                            heapq.heappush(PQ, (earliest_arrival_time[v], v))
            total = total + len(visited)
            if max_heap != [] and len(max_heap) >= k and total > max_heap[0][0]:
                return -1, x
        return total, x

    def top_k_reachability(self, alpha, beta, k, output_name):
        # start_time = time.time()
        # helper = [np.inf for _ in range(self.n)]
        # pool = multiprocessing.Pool(multiprocessing.cpu_count())
        # for node in self.nodes:
        #     pool.apply_async(self.top_k_util, args=(node, alpha, beta, helper), callback=log_result)
        # pool.close()
        # pool.join()
        # finish = time.time() - start_time
        # with open(path + output_name, 'w') as f:
        #     max_heap.sort()
        #     f.write(str(max_heap) + "\n")
        #     f.write("abgeschlossen in %s Sekunden" % finish + "\n")
        #     f.write("abgeschlossen in %s Minuten" % (finish / 60) + "\n")
        #     f.write("abgeschlossen in %s Stunden" % (finish / 3600))
        start_time = time.time()
        loop_counter = 0
        helper = [np.inf for _ in range(self.n)]
        for node in self.nodes:
            log_result(self.top_k_util(node, alpha, beta, helper, loop_counter))
        finish = time.time() - start_time
        with open(path + output_name, 'w') as f:
            max_heap.sort()
            f.write(str(max_heap) + "\n")
            f.write("Schleifendurchläufe: %s" % loop_counter + "\n")
            f.write("abgeschlossen in %s Sekunden" % finish + "\n")
            f.write("abgeschlossen in %s Minuten" % (finish / 60) + "\n")
            f.write("abgeschlossen in %s Stunden" % (finish / 3600))


if __name__ == '__main__':
    input_graph = input('Edgeliste eingeben:')
    output_file = input_graph.split(".")[0] + '-Top' + str(k) + '.txt'
    G = TemporalGraph()
    directed = (input('Soll die Kantenliste als gerichtet betrachtet werden? [y/n]:'))
    if directed == 'y':
        G.import_edgelist(input_graph)
    elif directed == 'n':
        G.import_undirected_edgelist(input_graph)
    G.top_k_reachability(0, np.inf, k, output_file)