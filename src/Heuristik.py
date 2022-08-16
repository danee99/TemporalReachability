import multiprocessing
import time
from queue import PriorityQueue
import heapq
import numpy as np
import os

# path = os.path.join(os.getcwd(), os.pardir) + "\\edge-lists\\"
path = "/home/stud/degenste/BA/TemporalReachability/edge-lists/"


class TemporalGraph:
    def __init__(self):
        self.n = 0
        self.m = 0
        # self.T = set()
        # self.Es = set()
        self.graph = {}
        self.reachability_change_of_deleted_nodes = 0
        self.num_deleted_nodes = 0

    def add_edge(self, u, v, t, l):
        if u not in self.graph:
            self.graph[u] = [[(u, v, t, l)], 1, 0]
        else:
            # if v not in [self.graph[u][0][i][1] for i in range(0, len(self.graph[u][0]))]:
            #     self.graph[u][1] += 1
            self.graph[u][1] += 1
            self.graph[u][0].append((u, v, t, l))
        if v not in self.graph:
            self.graph[v] = [[], 0, 0]
        self.m += 1
        # self.T.add(t)
        # self.Es.add((u, v))

    def print_graph(self):
        print("|V| = " + str(self.n) + ", |E| = " + str(self.m))
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

    def degrees_info(self):
        var = [self.graph[u][1] for u in self.graph]
        # print("& " + str(self.n) + " & " + str(self.m) + " & " + str(len(self.Es)) + " & " + str(len(self.T)) + " & " + str(
        #     round(sum(var) / len(var))) + " & " + str(int(min(var))) + " & " + str(int(max(var))))

    def degree_centrality(self, output_name):
        result = []
        with open(path + output_name, 'w') as f:
            for node in range(0, self.n):
                result.append(self.graph[node][1])
            f.write(str(result))

    def filter_nodes(self, depth):
        deleted_nodes = set()
        for i in range(0, depth):
            for node in self.graph:
                if self.graph[node][1] == 0:
                    deleted_nodes.add(node)
                    self.num_deleted_nodes += 1
                    self.graph[node][2] += 1
            for node in self.graph:
                visited = set()
                for (u, v, t, l) in self.graph[node][0][:]:
                    if v in deleted_nodes:
                        if v not in visited:
                            self.graph[node][2] += 1
                        self.graph[node][1] -= 1
                        self.graph[u][0].remove((u, v, t, l))
                        self.m -= 1
                        visited.add(v)
            while deleted_nodes:
                delete_me = deleted_nodes.pop()
                self.reachability_change_of_deleted_nodes += self.graph[delete_me][2]
                try:
                    del self.graph[delete_me]
                    self.n -= 1
                except KeyError:
                    continue

    def calculate_bounds(self, a, b, x):
        lower_bound = self.reachability_change_of_deleted_nodes
        # upper_bound = self.reachability_change_of_deleted_nodes
        for node in self.graph:
            if node == x:
                continue
            visited = set()
            earliest_arrival_time = {v: np.inf for v in self.graph}
            earliest_arrival_time[node] = a
            PQ = []
            heapq.heappush(PQ, (0, node))
            while PQ:
                (current_arrival_time, current_node) = heapq.heappop(PQ)
                if current_node != x:
                    visited.add(current_node)
                for (u, v, t, l) in self.graph[current_node][0]:
                    if u != x and v != x and v not in visited:
                        if t < a or t + l > b: continue
                        if t + l < earliest_arrival_time[v] and t >= current_arrival_time:
                            earliest_arrival_time[v] = t + l
                            heapq.heappush(PQ, (earliest_arrival_time[v], v))
            lower_bound += len(visited) + self.graph[node][2]
            # upper_bound += len(visited) + self.num_deleted_nodes
        # return x, (lower_bound, upper_bound)
        return lower_bound, x
        # return lower_bound, upper_bound, x

    def heuristik(self, a, b, output_name, depth, k):
        num_edges = self.m
        num_nodes = self.n
        start_time = time.time()
        self.filter_nodes(depth)
        finish1 = time.time() - start_time
        pool = multiprocessing.Pool(multiprocessing.cpu_count())
        result_objects = [pool.apply_async(self.calculate_bounds, args=(a, b, node)) for node
                          in self.graph]
        ranking = [r.get() for r in result_objects]
        pool.close()
        pool.join()
        finish2 = time.time() - start_time
        with open(path + output_name, 'w') as f:
            # f.write(str(ranking) + "\n")
            ranking.sort()
            f.write(str([v for (rank, v) in ranking[:k]]) + "\n")
            f.write("filter_nodes() abgeschlossen in %s Sekunden" % finish1 + "\n")
            f.write("geloeschte Knotenanzahl = " + str(num_nodes - self.n) + "\n")
            f.write("geloeschte Kanten = " + str(num_edges - self.m) + "\n")
            f.write("abgeschlossen in %s Minuten" % (finish2 / 60) + "\n")
            # f.write("mit Tiefe = " + str(depth) + "\n")
            # f.write("filter_nodes() abgeschlossen in %s Sekunden" % finish1 + "\n")
            # f.write("geloeschte Knotenanzahl = " + str(num_nodes - self.n) + "\n")
            # f.write("geloeschte Kanten = " + str(num_edges - self.m) + "\n")
            # f.write("abgeschlossen in %s Sekunden" % finish2 + "\n")
            # f.write("abgeschlossen in %s Minuten" % (finish2 / 60) + "\n")
            # f.write("abgeschlossen in %s Stunden" % (finish2 / 3600))
            # for i in range(len(ranking)):
            #     f.write(str(i + 1) + ".Platz: " + str(ranking[i][2]) + " mit " + str(ranking[i][0]) + " und " + str(
            #         ranking[i][1]) + "\n")


if __name__ == '__main__':
    input_graph = input('Edgeliste eingeben:')
    directed = (input('Ist der Graph gerichtet? [y/n]:'))
    depth = int(input('Tiefe eingeben:'))
    k = int(input('Top k Knoten, k eingeben:'))
    degree_output_file = input_graph.split(".")[0] + '-Outdegrees.txt'
    heuristik_output_file = input_graph.split(".")[0] + '-Heuristik-top-' + str(k) + '.txt'
    G = TemporalGraph()
    if directed == 'y':
        G.import_edgelist(input_graph)
    elif directed == 'n':
        G.import_undirected_edgelist(input_graph)
    G.heuristik(0, np.inf, heuristik_output_file, depth, k)
    # G.degrees_info()
    # G.degree_centrality(degree_output_file)
