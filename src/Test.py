import multiprocessing
import os
import time
import numpy as np
from heapdict import heapdict
from fibheap import *

# path = os.path.join(os.getcwd(), os.pardir) + "\\edge-lists\\"
path = "/home/stud/degenste/BA/TemporalReachability/edge-lists/"


# class MinHeap:
#     def __init__(self, arr=None):
#         self.heap = []
#         self.heap_size = 0
#         if arr is not None:
#             self.create_min_heap(arr)
#             self.heap = arr
#             self.heap_size = len(arr)
#
#     def build_min_heap(self, arr):
#         n = len(arr)
#         for i in range(int(n / 2), -1, -1):
#             self.min_heapify(i, arr, n)
#
#     def min_heapify(self, i, arr, size):
#         left_child = i * 2 + 1
#         right_child = i * 2 + 2
#         smallest = i
#         if left_child < size and arr[left_child][0] < arr[smallest][0]:
#             smallest = left_child
#         if right_child < size and arr[right_child][0] < arr[smallest][0]:
#             smallest = right_child
#         if smallest != i:
#             arr[i], arr[smallest] = arr[smallest], arr[i]
#             self.min_heapify(smallest, arr, size)
#
#     def insert(self, item):
#         self.heap.append(item)
#         self.heap_size += 1
#         i = self.heap_size - 1
#         parent = int(ceil(i / 2 - 1))
#         while parent >= 0 and self.heap[i][0] < self.heap[parent][0]:
#             self.heap[i], self.heap[parent] = self.heap[parent], self.heap[i]
#             i = parent
#             parent = int(ceil(i / 2 - 1))
#
#     def delete(self, i):
#         if self.heap_size == 0:
#             print("Heap Underflow!!")
#             return
#         self.heap[-1], self.heap[i] = self.heap[i], self.heap[-1]
#         self.heap_size -= 1
#         self.min_heapify(i, self.heap, self.heap_size)
#         return self.heap.pop()
#
#     # to do
#     def decrease_key(self, i):
#         return self.heap
#
#     def extract_min(self):
#         return self.delete(0)


class TemporalGraph:
    def __init__(self):
        self.nodes = []
        self.incidence_list = []
        self.n = 0
        self.m = 0
        self.total_reachability = 0

    def print_graph(self):
        for node in self.nodes:
            print(str(node) + ": " + str(self.incidence_list[node]))

    def import_edgelist(self, file_name):
        with open(path + file_name, "r") as f:
            n = int(f.readline())
            self.n = n
            self.incidence_list = [[] for _ in range(n)]
            self.nodes = [i for i in range(self.n)]
            for line in f:
                arr = line.split()
                u = int(arr[0])
                v = int(arr[1])
                t = int(arr[2])
                try:
                    l = int(arr[3])
                except IndexError:
                    l = 1
                self.incidence_list[u].append((u, v, t, l))
                self.m += 1

    def import_undirected_edgelist(self, file_name):
        with open(path + file_name, "r") as f:
            n = int(f.readline())
            self.n = n
            self.incidence_list = [[] for _ in range(self.n)]
            self.nodes = [i for i in range(self.n)]
            for line in f:
                arr = line.split()
                u = int(arr[0])
                v = int(arr[1])
                t = int(arr[2])
                try:
                    l = int(arr[3])
                except IndexError:
                    l = 1
                self.incidence_list[u].append((u, v, t, l))
                self.incidence_list[v].append((v, u, t, l))
                self.m += 2

    def calc_total_reachability(self, a, b):
        for node in self.nodes:
            visited = set()
            earliest_arrival_time = [np.inf for _ in range(self.n)]
            earliest_arrival_time[node] = a
            PQ = makefheap()
            fheappush(PQ, (0, node))
            while PQ.num_nodes:
                (current_arrival_time, current_node) = fheappop(PQ)
                visited.add(current_node)
                for (u, v, t, l) in self.incidence_list[current_node]:
                    if v not in visited:
                        if t < a or t + l > b: continue
                        if t + l < earliest_arrival_time[v] and t >= current_arrival_time:
                            if earliest_arrival_time[v] != np.inf:
                                PQ.decrease_key((v, earliest_arrival_time[v]), t + l)
                                earliest_arrival_time[v] = t + l
                            else:
                                earliest_arrival_time[v] = t + l
                                fheappush(PQ, (t + l, v))
            self.total_reachability += len(visited)

    def rank_node(self, x, a, b, before, helper):
        total = 0
        for node in self.nodes:
            if node == x:
                continue
            visited = set()
            earliest_arrival_time = helper.copy()
            earliest_arrival_time[node] = a
            PQ = makefheap()
            fheappush(PQ, (0, node))
            while PQ.num_nodes:
                (current_arrival_time, current_node) = fheappop(PQ)
                if current_node != x:
                    visited.add(current_node)
                for (u, v, t, l) in self.incidence_list[current_node]:
                    if u != x and v != x and v not in visited:
                        if t < a or t + l > b: continue
                        if t + l < earliest_arrival_time[v] and t >= current_arrival_time:
                            if earliest_arrival_time[v] != np.inf:
                                PQ.decrease_key((v, earliest_arrival_time[v]), t + l)
                                earliest_arrival_time[v] = t + l
                            else:
                                earliest_arrival_time[v] = t + l
                                fheappush(PQ, (t + l, v))
            total += len(visited)
        return 1 - (total / before), x

    def node_ranking(self, a, b, output_name):
        start_time = time.time()
        self.calc_total_reachability(a, b)
        helper = [np.inf for _ in range(self.n)]
        pool = multiprocessing.Pool(multiprocessing.cpu_count())
        result_objects = [pool.apply_async(self.rank_node, args=(node, a, b, self.total_reachability, helper))
                          for node in range(0, self.n)]
        ranking = [r.get() for r in result_objects]
        pool.close()
        pool.join()
        finish = time.time() - start_time
        with open(path + output_name, 'w') as f:
            ranking.sort(reverse=True)
            for i in range(len(ranking)):
                f.write(str(i + 1) + ".Platz: " + str(ranking[i][1]) + "\n")
            f.write("R(G) = %s" % self.total_reachability + "\n")
            f.write("abgeschlossen in %s Sekunden" % finish + "\n")
            f.write("abgeschlossen in %s Minuten" % (finish / 60) + "\n")
            f.write("abgeschlossen in %s Stunden" % (finish / 3600))


if __name__ == '__main__':
    input_graph = input('Edgeliste eingeben:')
    directed = (input('Soll die Kantenliste als gerichtet betrachtet werden? [y/n]:'))
    a = int(input('Intervall a eingeben: '))
    b = np.inf
    output_file = input_graph.split(".")[0] + '-Optimal-fib-heap.txt'
    G = TemporalGraph()
    if directed == 'y':
        G.import_edgelist(input_graph)
    elif directed == 'n':
        G.import_undirected_edgelist(input_graph)
    G.node_ranking(a, b, output_file)
