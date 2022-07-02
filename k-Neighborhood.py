import multiprocessing
import os
from queue import PriorityQueue
import numpy as np
import time


class TemporalGraph:
    def __init__(self):
        self.n = 0
        self.m = 0
        self.graph = {}
        self.total_reachability = 0

    def add_edge(self, u, v, t, l):
        if u not in self.graph:
            self.graph[u] = [(u, v, t, l)]
        else:
            self.graph[u].append((u, v, t, l))
        if v not in self.graph:
            self.graph[v] = []
        self.m += 1

    def print_graph(self):
        print("|V| = " + str(self.n) + " |E| = " + str(self.m))
        for v in self.graph:
            print(str(v) + " " + str(self.graph[v]))

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
                self.add_edge(v, u, t, l)

    def import_undirected_edgelist(self, file_name):
        with open(os.getcwd() + file_name, "r") as f:
            self.n = int(f.readline())
            for line in f:
                arr = line.split()
                u = int(arr[0])
                v = int(arr[1])
                t = int(arr[2])
                l = int(arr[3])
                self.add_edge(u, v, t, l)

    # def staic_bfs(self, node):
    #     visited = [node]
    #     queue = []
    #     queue.append(node)
    #     while queue:
    #         current_node = queue.pop(0)
    #         for (current_node, neighbour, t, l) in self.graph[current_node]:
    #             if neighbour not in visited:
    #                 visited.append(neighbour)
    #                 queue.append(neighbour)
    #     return visited

    def k_neighborhood(self, node, k):
        visited = set()
        queue = [node, -1]
        i = 0
        while queue:
            current_node = queue.pop(0)
            if current_node == -1:
                i += 1
                queue.append(-1)
                if i == k:
                    break
                else:
                    continue
            else:
                for (current_node, neighbour, t, l) in self.graph[current_node]:
                    if neighbour not in visited:
                        visited.add(neighbour)
                        queue.append(neighbour)
        return visited

    def total_reachability_after(self, deleted_node, a, b, k):
        total = 0
        # bfs_start_time = time.time()
        k_neighbours = self.k_neighborhood(deleted_node, k)
        # bfs_finish_time = time.time() - bfs_start_time
        for node in k_neighbours:
            if node == deleted_node:
                continue
            reach_set = {node}
            visited = set()
            earliest_arrival_time = {c: np.inf for c in k_neighbours}
            earliest_arrival_time[node] = 0
            PQ = PriorityQueue()
            PQ.put((earliest_arrival_time[node], node))
            while not PQ.empty():
                (current_arrival_time, current_node) = PQ.get()
                if current_node not in visited:
                    for (u, v, t, l) in self.graph[current_node]:
                        if u not in k_neighbours or v not in k_neighbours:
                            continue
                        if v != deleted_node and u != deleted_node:
                            if t < a or t + l > b: continue
                            if t + l < earliest_arrival_time[v] and t >= current_arrival_time:
                                reach_set.add(v)
                                earliest_arrival_time[v] = t + l
                                PQ.put((earliest_arrival_time[v], v))
                    visited.add(current_node)
            # print(node, len(reach_set))
            total += len(reach_set)
        # print(str(bfs_finish_time) + " Sekunden")
        return total


if __name__ == '__main__':
    input_graph = '/edge-lists/' + input('Edgeliste eingeben:')
    k = int(input('k-Nachbarschaft, Gebe den Wert k ein:'))
    output_file = input_graph.split(".")[0] + '-k-Nachbarschaft-Ranking' + '.txt'
    G = TemporalGraph()
    G.import_undirected_edgelist(input_graph)
    start_time = time.time()
    pool = multiprocessing.Pool(multiprocessing.cpu_count())
    result_objects = [pool.apply_async(G.total_reachability_after, args=(node, 0, np.inf, k)) for node in range(0, G.n)]
    ranking = [r.get() for r in result_objects]
    pool.close()
    pool.join()
    finish = time.time() - start_time
    with open(os.getcwd() + output_file, 'w') as f:
        f.write(str(ranking) + "\n")
        f.write("wurde auf die " + str(k) + "-Nachbarschaft jedes Knotens angewendet." + "\n")
        f.write("|V| = " + str(G.n) + ", |E| = " + str(G.m) + "\n")
        f.write("--- finished in %s seconds ---" % finish + "\n")
        f.write("--- finished in %s minutes ---" % (finish / 60) + "\n")
        f.write("--- finished in %s hours ---" % (finish / 3600))
