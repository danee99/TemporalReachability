import multiprocessing
import time
from queue import PriorityQueue
import heapq
import numpy as np
import os

path = os.path.join(os.getcwd(), os.pardir) + "\\edge-lists\\"
# path = "/home/stud/degenste/BA/TemporalReachability/edge-lists/"

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
        with open(path + file_name, "r") as f:
            self.n = int(f.readline())
            for line in f:
                arr = line.split()
                u = int(arr[0])
                v = int(arr[1])
                t = int(arr[2])
                l = int(arr[3])
                self.add_edge(u, v, t, l)

    def import_undirected_edgelist(self, file_name):
        with open(path + file_name, "r") as f:
            self.n = int(f.readline())
            for line in f:
                arr = line.split()
                u = int(arr[0])
                v = int(arr[1])
                t = int(arr[2])
                l = int(arr[3])
                self.add_edge(u, v, t, l)
                self.add_edge(v, u, t, l)

    def k_neighborhood_subgraph(self, node, k):
        sub_graph = {node: []}
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
                for (u, neighbour, t, l) in self.graph[current_node]:
                    if neighbour not in sub_graph:
                        sub_graph[neighbour] = []
                        queue.append(neighbour)
        for x in sub_graph:
            sub_graph[x] = [(u, v, t, l) for (u, v, t, l) in self.graph[x] if v in sub_graph]
        return sub_graph

    def total_reachability_after(self, deleted_node, a, b, k, p):
        total = 0
        k_neighbours = self.k_neighborhood_subgraph(deleted_node, k)
        before = 0
        size = len(k_neighbours)
        size_alt = size - 1
        if size <= p:
            return 0, deleted_node, size
        for node in k_neighbours:
            visited = set()
            earliest_arrival_time = {j: np.inf for j in k_neighbours}
            earliest_arrival_time[node] = a
            PQ = []
            heapq.heappush(PQ, (earliest_arrival_time[node], node))
            while PQ:
                (current_arrival_time, current_node) = heapq.heappop(PQ)
                visited.add(current_node)
                for (u, v, t, l) in k_neighbours[current_node]:
                    if v not in visited:
                        if t < a or t + l > b: continue
                        if t + l < earliest_arrival_time[v] and t >= current_arrival_time:
                            earliest_arrival_time[v] = t + l
                            heapq.heappush(PQ, (earliest_arrival_time[v], v))
            before += len(visited)
        for node in k_neighbours:
            if node == deleted_node:
                continue
            visited = set()
            earliest_arrival_time = {j: np.inf for j in k_neighbours}
            earliest_arrival_time[node] = a
            PQ = []
            heapq.heappush(PQ, (0, node))
            while PQ:
                (current_arrival_time, current_node) = heapq.heappop(PQ)
                if current_node != deleted_node:
                    visited.add(current_node)
                for (u, v, t, l) in k_neighbours[current_node]:
                    if v not in visited:
                        if v != deleted_node and u != deleted_node:
                            if t < a or t + l > b: continue
                            if t + l < earliest_arrival_time[v] and t >= current_arrival_time:
                                earliest_arrival_time[v] = t + l
                                heapq.heappush(PQ, (earliest_arrival_time[v], v))
            total += len(visited)
        if total < size:
            return 0, deleted_node, size
        rank = 1 - (total * size) / (before * size_alt)
        if rank < 0:
            return 0, deleted_node, size
        else:
            return rank, deleted_node, size
        # return total, deleted_node, size


if __name__ == '__main__':
    input_graph = input('Edgeliste eingeben:')
    k = int(input('k-Nachbarschaft, Gebe den Wert k ein:'))
    p = int(input('Schranke für die Größe der Nachbarschaft:'))
    j = int(input('top k, k eingeben:'))
    directed = (input('Ist das Format der Kantenliste bereits ungerichtet? [y/n]:'))
    output_file = input_graph.split(".")[0] + '-k-Nachbarschaft-Ranking-top-' + str(j) + '.txt'
    G = TemporalGraph()
    if directed == 'y':
        G.import_edgelist(input_graph)
    elif directed == 'n':
        G.import_undirected_edgelist(input_graph)
    start_time = time.time()
    pool = multiprocessing.Pool(multiprocessing.cpu_count())
    result_objects = [pool.apply_async(G.total_reachability_after, args=(node, 0, np.inf, k, p)) for node in
                      range(0, G.n)]
    result = [r.get() for r in result_objects]
    pool.close()
    pool.join()
    finish = time.time() - start_time
    with open(path + output_file, 'w') as f:
        result.sort(reverse=True)
        f.write(str(str([v for (ranking, v, size) in result[:j]]) + "\n"))
        f.write("wurde auf die " + str(k) + "-Nachbarschaft jedes Knotens angewendet." + "\n")
        f.write("Schwellwert fuer die Groesse der Nachbaschaft: " + str(p) + "\n")
        f.write("|V| = " + str(G.n) + ", |E| = " + str(G.m) + "\n")
        f.write("abgeschlossen in %s Sekunden" % finish + "\n")
        f.write("abgeschlossen in %s Minuten" % (finish / 60) + "\n")
        f.write("abgeschlossen in %s Stunden" % (finish / 3600))

        # result.sort()
        # f.write(str(result) + "\n")
        # f.write("wurde auf die " + str(k) + "-Nachbarschaft jedes Knotens angewendet." + "\n")
        # f.write("Schwellwert für die Größe der Nachbaschaft: " + str(p) + "\n")
        # f.write("|V| = " + str(G.n) + ", |E| = " + str(G.m) + "\n")
        # f.write("abgeschlossen in %s Sekunden" % finish + "\n")
        # f.write("abgeschlossen in %s Minuten" % (finish / 60) + "\n")
        # f.write("abgeschlossen in %s Stunden" % (finish / 3600))

        # f.write("abgeschlossen in %s Minuten" % (finish / 60) + "\n")
        # f.write("wurde auf die " + str(k) + "-Nachbarschaft jedes Knotens angewendet." + "\n")
        # result.sort(reverse=True)
        # for i in range(len(result)):
        #     f.write(str(i + 1) + ".Platz: " + str(result[i][1]) + " mit rank(u) = " + str(
        #         result[i][0]) + " und |K| = " + str(result[i][2]) + "\n")
