import multiprocessing
import os
import time
from queue import PriorityQueue
import heapq_max
import numpy as np

max_heap = []
k = 10
path = os.path.join(os.getcwd(), os.pardir) + "\\edge-lists\\"


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

    def top_k_util(self, x, alpha, beta):
        total = 0
        for node in self.nodes:
            if node == x:
                continue
            reach_set = {node}
            visited = set()
            earliest_arrival_time = [np.inf for _ in range(self.n)]
            earliest_arrival_time[node] = alpha
            PQ = PriorityQueue()
            PQ.put((earliest_arrival_time[node], node))
            while not PQ.empty():
                (current_arrival_time, current_node) = PQ.get()
                if current_node not in visited:
                    for (u, v, t, l) in self.incidence_list[current_node]:
                        if u != x and v != x:
                            if t < alpha or t + l > beta: continue
                            if t + l < earliest_arrival_time[v] and t >= current_arrival_time:
                                reach_set.add(v)
                                earliest_arrival_time[v] = t + l
                                PQ.put((earliest_arrival_time[v], v))
                    visited.add(current_node)
            total = total + len(reach_set)
            if max_heap != [] and len(max_heap) >= k and total > max_heap[0][0]:
                return -1, x
        return total, x

    def top_k_reachability(self, alpha, beta, k, output_name):
        start_time = time.time()
        pool = multiprocessing.Pool(multiprocessing.cpu_count())
        for node in self.nodes:
            pool.apply_async(self.top_k_util, args=(node, alpha, beta), callback=log_result)
        pool.close()
        pool.join()
        finish = time.time() - start_time
        with open(path + output_name, 'w') as f:
            max_heap.sort(key=lambda tup: tup[0])
            f.write(str(max_heap) + "\n")
            f.write("abgeschlossen in %s Sekunden" % finish + "\n")
            f.write("abgeschlossen in %s Minuten" % (finish / 60) + "\n")
            f.write("abgeschlossen in %s Stunden" % (finish / 3600))
        # start_time = time.time()
        # for p in self.nodes:
        #     total = 0
        #     for node in self.nodes:
        #         if node == p:
        #             continue
        #         reach_set = {node}
        #         visited = set()
        #         earliest_arrival_time = [np.inf for _ in range(self.n)]
        #         earliest_arrival_time[node] = alpha
        #         PQ = PriorityQueue()
        #         PQ.put((earliest_arrival_time[node], node))
        #         while not PQ.empty():
        #             (current_arrival_time, current_node) = PQ.get()
        #             if current_node not in visited:
        #                 for (u, v, t, l) in self.incidence_list[current_node]:
        #                     if u != p and v != p:
        #                         if t < alpha or t + l > beta: continue
        #                         if t + l < earliest_arrival_time[v] and t >= current_arrival_time:
        #                             reach_set.add(v)
        #                             earliest_arrival_time[v] = t + l
        #                             PQ.put((earliest_arrival_time[v], v))
        #                 visited.add(current_node)
        #         total = total + len(reach_set)
        #         if max_heap != [] and len(max_heap) >= k and total > max_heap[0][0]:
        #             break
        #     if len(max_heap) < k:
        #         heapq_max.heappush_max(max_heap, (total, p))
        #     if len(max_heap) >= k:
        #         if total < max_heap[0][0]:
        #             heapq_max.heappushpop_max(max_heap, (total, p))
        # finish = time.time() - start_time
        # with open(path + output_name, 'w') as f:
        #     f.write(str(max_heap) + "\n")
        #     f.write("abgeschlossen in %s Sekunden" % finish + "\n")
        #     f.write("abgeschlossen in %s Minuten" % (finish / 60) + "\n")
        #     f.write("abgeschlossen in %s Stunden" % (finish / 3600))


if __name__ == '__main__':
    input_graph = input('Edgeliste eingeben:')
    output_file = input_graph.split(".")[0] + '-Top' + str(k) + '.txt'
    G = TemporalGraph()
    G.import_edgelist(input_graph)
    G.top_k_reachability(0, np.inf, k, output_file)
