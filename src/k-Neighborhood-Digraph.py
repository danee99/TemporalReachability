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
        self.graph = {}
        self.total_reachability = 0

    def add_edge(self, u, v, t, l):
        if u not in self.graph:
            self.graph[u] = [[(u, v, t, l)], set()]
        else:
            self.graph[u][0].append((u, v, t, l))
        if v not in self.graph:
            self.graph[v] = [[], set()]
        self.graph[u][1].add(v)
        self.graph[v][1].add(u)
        self.m += 1

    def neighbors_of(self, node):
        return self.graph[node][1]

    def DFS(self, v, visited):
        visited[v] = True
        for u in self.neighbors_of(v):
            if not visited[u]:
                self.DFS(u, visited)

    def is_connected(self):
        for i in self.graph:
            visited = [False] * self.n
            self.DFS(i, visited)
            for b in visited:
                if not b:
                    return False
        return True

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

    def k_neighborhood(self, node, k):
        # Ausgabe: Menge der Knoten, die sich in der k-Nachbarschaft von "node" befinden
        visited = set()
        visited.add(node)
        queue = [node, -1]
        i = 0
        # Idee: i immer um 1 erhöhen, wenn die Breitensuche die nächste Tiefe erreicht.
        # Wann weiß man, dass die nächste Tiefe erreicht wurde? Wenn -1 aus der Warteschlange genommen wurde!
        # Wenn das aus der Warteschlange genommene Element -1 ist, weiß man, dass die i-Nachbarschaft erkundet wurde!
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
                for neighbour in self.neighbors_of(current_node):
                    if neighbour not in visited:
                        visited.add(neighbour)
                        queue.append(neighbour)
        return visited

    def k_neighborhood_subgraph(self, node, k):
        sub_graph = {node: []}
        queue = [node, -1]
        i = 0
        while queue:
            current_node = queue.pop(0)
            if current_node == -1:
                i += 1
                queue.append(-1)
                if i >= k:
                    break
                else:
                    continue
            else:
                for neighbour in self.neighbors_of(current_node):
                    if neighbour not in sub_graph:
                        sub_graph[neighbour] = []
                        queue.append(neighbour)
        for u in sub_graph:
            sub_graph[u] = [(u, v, t, l) for (u, v, t, l) in self.graph[u][0] if v in sub_graph]
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
                S = {current_node}
                for (u, v, t, l) in k_neighbours[current_node]:
                    if v not in visited and v not in S:
                        if t < a or t + l > b: continue
                        if t + l < earliest_arrival_time[v] and t >= current_arrival_time:
                            earliest_arrival_time[v] = t + l
                            heapq.heappush(PQ, (earliest_arrival_time[v], v))
                            S.add(v)
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
                S = {current_node}
                for (u, v, t, l) in k_neighbours[current_node]:
                    if v not in visited and v not in S:
                        if v != deleted_node and u != deleted_node:
                            if t < a or t + l > b: continue
                            if t + l < earliest_arrival_time[v] and t >= current_arrival_time:
                                earliest_arrival_time[v] = t + l
                                heapq.heappush(PQ, (earliest_arrival_time[v], v))
                                S.add(v)
            total += len(visited)
        if total < size:
            return 0, deleted_node, size
        rank = 1 - (total * size) / (before * size_alt)
        if rank < 0:
            return 0, deleted_node, size
        else:
            return rank, deleted_node, size


if __name__ == '__main__':
    input_graph = input('Edgeliste eingeben:')
    k = int(input('k-Nachbarschaft, Gebe den Wert k ein:'))
    p = int(input('Schranke für die Größe der Nachbarschaft:'))
    output_file = input_graph.split(".")[0] + '-k-Nachbarschaft-Ranking (Digraph)-top-' + str(1000) + '.txt'
    G = TemporalGraph()
    G.import_edgelist(input_graph)
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
        f.write(str([v for (ranking, v, size) in result]) + "\n")
        sizes = [size for (ranking, v, size) in result]
        f.write("Durchschnitt |K| = " + str(str(round(sum(sizes) / len(sizes))) + "\n"))
        f.write("wurde auf die " + str(k) + "-Nachbarschaft jedes Knotens angewendet." + "\n")
        f.write("Schwellwert fuer die Groesse der Nachbaschaft: " + str(p) + "\n")
        f.write("abgeschlossen in %s Sekunden" % finish + "\n")
        f.write("abgeschlossen in %s Minuten" % (finish / 60) + "\n")
        f.write("abgeschlossen in %s Stunden" % (finish / 3600))
