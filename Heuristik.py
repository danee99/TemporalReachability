import multiprocessing
import os
import time
from queue import PriorityQueue
import heapq_max
import numpy as np
import copy
from timeit import default_timer as timer

max_heap = []
k = 11


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

    def k_core_decomposition1(self):
        core = [None for _ in range(self.n)]
        deg = self.outdegree.copy()
        V = list(map(lambda x, y: (x, y), self.nodes, self.outdegree))
        V.sort(key=lambda a: a[1])
        for (v, degree) in V:
            core[v] = self.outdegree[v]
            for edge in self.incidence_list[v]:
                if deg[edge[1]] > deg[v]:
                    deg[edge[1]] = deg[edge[1]] - 1
                    V.sort(key=lambda a: a[1])
        print(deg)

    def k_core_decomposition2(self):
        n = self.n
        # compute the degree for each node v and store it in the array deg
        # at the same time calculate the maximum degree md
        deg = self.outdegree.copy()
        md = max(self.outdegree)
        md += 1

        # vert = contains the set of nodes sorted by their degree
        # pos = contains the positions of the nodes in the array vert
        # bin = contains for each possible degree the position of the first occurring node with this degree
        # now sort the nodes in ascending order of their degree with bin-sort.
        # to do this, first count how many nodes will be in each bin.
        bin = [0] * md
        for v in range(n):
            bin[deg[v]] += 1
        # using the bin sizes, we can determine the starting positions of the bins in the array vert
        start = 0
        for d in range(md):
            num = bin[d]
            bin[d] = start
            start += num
        valBucket = [0] * md
        vert = [0] * n
        pos = [0] * n
        # insert nodes into the array vert
        # for each node we know to which field it belongs and what is the starting position of this field
        # so now we can sort the nodes by their degree
        for v in range(n):
            pos[v] = bin[deg[v]] + valBucket[deg[v]]
            vert[pos[v]] = v
            valBucket[deg[v]] += 1
        # now comes the core decomposition
        # at first, the core number of node v its degree
        # for each neighbor u of the node v with higher degree we must decrease its degree
        # in addition, it must be shifted one field to the left
        # the shift can be done in constant time:
        # --> swap node u and the first node in the field
        # --> in the field pos we have to swap their positions too
        # --> increase the initial position of the bin
        for i in range(n):
            v = vert[i]
            for edge in G.incidence_list[v]:
                u = edge[1]
                if deg[u] > deg[v]:
                    du = deg[u]
                    pu = pos[u]
                    pw = bin[du]
                    w = vert[pw]
                    if u != w:
                        pos[u] = pw
                        vert[pu] = w
                        pos[w] = pu
                        vert[pw] = u
                    bin[du] += 1
                    deg[u] -= 1
        print(deg)

    def k_core_decomposition3(self, k):
        for node in range(0, self.n):
            if self.outdegree[node] == 0:
                self.deleted_nodes.add(node)
                continue
            for edge in self.incidence_list[node]:
                if self.outdegree[edge[1]] < k:
                    self.incidence_list[node].remove(edge)
                    self.outdegree[node] -= 1
        self.print_graph()

    def k_core_decomposition4(self, k):
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

    # def largest_outdegrees(self, n):
    #     self.outdegree.sort(reverse=True)
    #     print(self.outdegree[:n][-1])
    #     print(max(self.outdegree, key=self.outdegree.count))
    #     print(self.outdegree)

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
        self.k_core_decomposition4(1)
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
            f.write("--- finished in %s hours ---" % (finish / 3600))
            f.write(str(max_heap) + "\n")
            f.write(str([element[1] for element in max_heap]) + "\n")
            f.write("gelöschte Knoten Anzahl " + str(len(self.deleted_nodes)) + "\n")
            f.write("Knotenanzahl des Graphen " + str(len(self.nodes)) + "\n")


if __name__ == '__main__':
    input_graph = '/edge-lists/' + input('Edgeliste eingeben:')
    output_file = input_graph.split(".")[0] + '-Heuristik-Top-' + str(k) + '.txt'
    G = TemporalGraph([], [])
    G.import_edgelist(input_graph)
    G.top_k_reachability(0, np.inf, k, output_file)
