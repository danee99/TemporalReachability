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
            # change
            self.graph[u] = [[(u, v, t, l)], set()]
        else:
            # change
            self.graph[u][0].append((u, v, t, l))
        if v not in self.graph:
            # change
            self.graph[v] = [[], set()]
        # change
        self.graph[u][1].add(v)
        # change
        self.graph[v][1].add(u)
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

    def k_neighborhood(self, node, k):
        visited = set()
        queue = [node, -1]
        i = 0
        # There are two possibilities for the algorithm to terminate
        # either the queue is empty, then every node of the graph (for example k=|V|) has been processed
        # or the k-neighborhood of node has been completely processed
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
                # change
                for neighbour in self.graph[current_node][1]:
                    if neighbour not in visited:
                        visited.add(neighbour)
                        queue.append(neighbour)
        return visited

    def total_reachability_after(self, deleted_node, a, b, k):
        total = 0
        k_neighbours = self.k_neighborhood(deleted_node, k)
        for node in k_neighbours:
            if node == deleted_node:
                continue
            reach_set = {node}
            visited = set()
            earliest_arrival_time = {j: np.inf for j in k_neighbours}
            earliest_arrival_time[node] = 0
            PQ = PriorityQueue()
            PQ.put((earliest_arrival_time[node], node))
            while not PQ.empty():
                (current_arrival_time, current_node) = PQ.get()
                if current_node not in visited:
                    # change
                    for (u, v, t, l) in self.graph[current_node][0]:
                        if u in k_neighbours and v in k_neighbours:
                            if v != deleted_node and u != deleted_node:
                                if t < a or t + l > b: continue
                                if t + l < earliest_arrival_time[v] and t >= current_arrival_time:
                                    reach_set.add(v)
                                    earliest_arrival_time[v] = t + l
                                    PQ.put((earliest_arrival_time[v], v))
                    visited.add(current_node)
            total += len(reach_set)
        return total


if __name__ == '__main__':
    input_graph = '/edge-lists/' + input('Edgeliste eingeben:')
    k = int(input('k-Nachbarschaft, Gebe den Wert k ein:'))
    output_file = input_graph.split(".")[0] + '-k-Nachbarschaft-Ranking' + '.txt'
    G = TemporalGraph()
    G.import_edgelist(input_graph)

    start_time = time.time()
    pool = multiprocessing.Pool(multiprocessing.cpu_count())
    result_objects = [pool.apply_async(G.total_reachability_after, args=(node, 0, np.inf, k)) for node in range(0, G.n)]
    result = [r.get() for r in result_objects]
    pool.close()
    pool.join()
    finish = time.time() - start_time
    with open(os.getcwd() + output_file, 'w') as f:
        f.write(str(result) + "\n")
        f.write("wurde auf die " + str(k) + "-Nachbarschaft jedes Knotens angewendet." + "\n")
        f.write("|V| = " + str(G.n) + ", |E| = " + str(G.m) + "\n")
        f.write("--- finished in %s seconds ---" % finish + "\n")
        f.write("--- finished in %s minutes ---" % (finish / 60) + "\n")
        f.write("--- finished in %s hours ---" % (finish / 3600))
