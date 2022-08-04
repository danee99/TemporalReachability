import multiprocessing
import time
from queue import PriorityQueue
import numpy as np
import os

# path = os.path.join(os.getcwd(), os.pardir) + "\\edge-lists\\"
path = "/home/stud/degenste/BA/TemporalReachability/edge-lists/"


class TemporalGraph:
    def __init__(self):
        self.n = 0
        self.m = 0
        self.nodes = []
        self.edge_stream = []
        self.total_reachability = 0

    def add_edge(self, u, v, t, l):
        self.edge_stream.append((u, v, t, l))
        self.nodes[u].add(v)
        self.nodes[v].add(u)
        self.m += 1

    def import_edgelist(self, file_name):
        with open(path + file_name, "r") as f:
            self.n = int(f.readline())
            self.nodes = [set() for _ in range(self.n)]
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
            self.nodes = [set() for _ in range(self.n)]
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
                for neighbour in self.nodes[current_node]:
                    if neighbour not in sub_graph:
                        sub_graph[neighbour] = []
                        queue.append(neighbour)
        for x in sub_graph:
            sub_graph[x] = [(u, v, t, l) for (u, v, t, l) in self.edge_stream if v in sub_graph]
        return sub_graph

    def rank_node(self, deleted_node, a, b, k, p):
        total = 0
        before = 0
        subgraph = self.k_neighborhood_subgraph(deleted_node, k)
        size = len(subgraph)
        if size <= p:
            return 0, deleted_node
        for node in self.nodes:
            reach_num = 1
            arrival_time = [np.inf for _ in range(self.n)]
            arrival_time[node] = a
            for (u, v, t, l) in self.edge_stream:
                if t >= a and b >= l:
                    if arrival_time[u] <= t and arrival_time[v] > t + l:
                        arrival_time[v] = t + l
                        reach_num = reach_num + 1
            total = total + reach_num
        for node in self.nodes:
            if node == deleted_node:
                continue
            reach_num = 1
            arrival_time = {j: np.inf for j in subgraph}
            arrival_time[node] = a
            for (u, v, t, l) in self.edge_stream:
                if u != deleted_node and v != deleted_node:
                    if t < a or t + l > b: continue
                    if arrival_time[u] <= t and arrival_time[v] > t + l:
                        arrival_time[v] = t + l
                        reach_num = reach_num + 1
            before += reach_num
        try:
            z = (total / before) * (size / (size - 1))
        except ZeroDivisionError:
            z = 1
        rank = 1 - z
        if rank < 0:
            return 0, deleted_node
        else:
            return rank, deleted_node


if __name__ == '__main__':
    input_graph = input('Edgeliste eingeben:')
    k = int(input('k-Nachbarschaft, Gebe den Wert k ein:'))
    p = int(input('Schranke für die Größe der Nachbarschaft:'))
    directed = (input('Ist das Format der Kantenliste bereits ungerichtet? [y/n]:'))
    output_file = input_graph.split(".")[0] + '-k-Nachbarschaft-Ranking' + '.txt'
    G = TemporalGraph()
    if directed == 'y':
        G.import_edgelist(input_graph)
    elif directed == 'n':
        G.import_undirected_edgelist(input_graph)
    start_time = time.time()
    pool = multiprocessing.Pool(multiprocessing.cpu_count())
    result_objects = [pool.apply_async(G.rank_node, args=(i, 0, np.inf, k, p)) for i in
                      range(0, G.n)]
    result = [r.get() for r in result_objects]
    pool.close()
    pool.join()
    finish = time.time() - start_time
    with open(path + output_file, 'w') as f:
        # result.sort()
        # f.write(str(result) + "\n")
        # f.write("wurde auf die " + str(k) + "-Nachbarschaft jedes Knotens angewendet." + "\n")
        # f.write("Schwellwert für die Größe der Nachbaschaft: " + str(p) + "\n")
        # f.write("|V| = " + str(G.n) + ", |E| = " + str(G.m) + "\n")
        # f.write("abgeschlossen in %s Sekunden" % finish + "\n")
        # f.write("abgeschlossen in %s Minuten" % (finish / 60) + "\n")
        # f.write("abgeschlossen in %s Stunden" % (finish / 3600))
        f.write("abgeschlossen in %s Minuten" % (finish / 60) + "\n")
        f.write("wurde auf die " + str(k) + "-Nachbarschaft jedes Knotens angewendet." + "\n")
        result.sort(reverse=True)
        for i in range(len(result)):
            f.write(str(i + 1) + ".Platz: " + str(result[i][1]) + " mit " + str(result[i][0]) + "\n")
