import multiprocessing
import os
import time
from queue import PriorityQueue
import heapq
import numpy as np

# path = os.path.join(os.getcwd(), os.pardir) + "\\edge-lists\\"
path = "/home/stud/degenste/BA/TemporalReachability/edge-lists/"

class TemporalGraph:
    def __init__(self):
        self.nodes = set()
        self.incidence_list = []
        self.n = 0
        self.m = 0
        self.total_reachability = 0

    # prints each node and the corresponding set of outgoing edges of the node
    def print_graph(self):
        for node in self.nodes:
            print(str(node) + ": " + str(self.incidence_list[node]))

    # scans an edgelist and creates a TemporalGraph object in O(n+m)
    def import_edgelist(self, file_name):
        with open(path + file_name, "r") as f:
            n = int(f.readline())
            self.n = n
            self.incidence_list = [[] for _ in range(n)]
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
                self.m += 1

    # scans an edgelist and creates a undirected temporal Graph in O(n+m)
    # Here, the edge list is assumed to have no back edges, even though the graph is undirected
    def import_undirected_edgelist(self, file_name):
        with open(path + file_name, "r") as f:
            n = int(f.readline())
            self.n = n
            self.incidence_list = [[] for _ in range(n)]
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
                self.m += 2

    # calculates for a given node "source" the number of nodes that "source" can reach
    def number_of_reachable_nodes(self, source, a, b):
        visited = set()
        earliest_arrival_time = [np.inf for _ in range(self.n)]
        earliest_arrival_time[source] = a
        PQ = []
        heapq.heappush(PQ, (0, source))
        while PQ:
            (current_arrival_time, current_node) = heapq.heappop(PQ)
            visited.add(current_node)
            for (u, v, t, l) in self.incidence_list[current_node]:
                if v not in visited:
                    if t < a or t + l > b: continue
                    if t + l < earliest_arrival_time[v] and t >= current_arrival_time:
                        earliest_arrival_time[v] = t + l
                        heapq.heappush(PQ, (earliest_arrival_time[v], v))
        return len(visited)

    # calculates the total reachability of the given temporal graph in a time interval [a,b]
    def calc_total_reachability(self, a, b):
        for node in self.nodes:
            visited = set()
            earliest_arrival_time = [np.inf for _ in range(self.n)]
            earliest_arrival_time[node] = a
            PQ = []
            heapq.heappush(PQ, (0, node))
            while PQ:
                (current_arrival_time, current_node) = heapq.heappop(PQ)
                visited.add(current_node)
                if self.incidence_list[current_node]:
                    for (u, v, t, l) in self.incidence_list[current_node]:
                        if v not in visited:
                            if t < a or t + l > b: continue
                            if t + l < earliest_arrival_time[v] and t >= current_arrival_time:
                                earliest_arrival_time[v] = t + l
                                heapq.heappush(PQ, (earliest_arrival_time[v], v))
                else:
                    continue
            self.total_reachability += len(visited)

    # ranks the node "x", where the ranking is a floating point number between 0 and 1
    def rank_node(self, x, a, b, before, helper, average):
        total = 0
        for node in self.nodes:
            if node == x:
                continue
            visited = set()
            earliest_arrival_time = helper.copy()
            earliest_arrival_time[node] = a
            PQ = []
            heapq.heappush(PQ, (0, node))
            while PQ:
                (current_arrival_time, current_node) = heapq.heappop(PQ)
                if current_node != x:
                    visited.add(current_node)
                if self.incidence_list[current_node]:
                    for (u, v, t, l) in self.incidence_list[current_node]:
                        if u != x and v != x and v not in visited:
                            if t < a or t + l > b: continue
                            if t + l < earliest_arrival_time[v] and t >= current_arrival_time:
                                earliest_arrival_time[v] = t + l
                                heapq.heappush(PQ, (earliest_arrival_time[v], v))
                else:
                    continue
            total += len(visited)
        # return 1 - (total / before)
        return total, x

    # parallelized node ranking
    def node_ranking(self, a, b, output_name):
        start_time = time.time()
        self.calc_total_reachability(a, b)
        helper = [np.inf for _ in range(self.n)]
        pool = multiprocessing.Pool(multiprocessing.cpu_count())
        result_objects = [pool.apply_async(self.rank_node, args=(node, a, b, self.total_reachability, helper, average)) for node
                          in range(0, self.n)]
        ranking = [r.get() for r in result_objects]
        pool.close()
        pool.join()
        finish = time.time() - start_time
        with open(path + output_name, 'w') as f:
            ranking.sort(reverse=False)
            for i in range(len(ranking)):
                f.write(str(i+1)+".Platz: "+str(ranking[i][1])+" mit R(G-v) = "+str(ranking[i][0]) + "\n")
            # f.write(str(ranking) + "\n")
            f.write("R(G) = %s" % self.total_reachability + "\n")
            f.write("abgeschlossen in %s Sekunden" % finish + "\n")
            f.write("abgeschlossen in %s Minuten" % (finish / 60) + "\n")
            f.write("abgeschlossen in %s Stunden" % (finish / 3600))
        # start_time = time.time()
        # self.calc_total_reachability(a, b)
        # helper = [np.inf for _ in range(self.n)]
        # ranking = []
        # for node in range(0, self.n):
        #     ranking.append(self.rank_node(node, a, b, self.total_reachability, helper))
        # finish = time.time() - start_time
        # with open(path + output_name, 'w') as f:
        #     f.write(str(ranking) + "\n")
        #     f.write("R(G) = %s" % self.total_reachability + "\n")
        #     f.write("abgeschlossen in %s Sekunden" % finish + "\n")
        #     f.write("abgeschlossen in %s Minuten" % (finish / 60) + "\n")
        #     f.write("abgeschlossen in %s Stunden" % (finish / 3600))


if __name__ == '__main__':
    input_graph = input('Edgeliste eingeben:')
    directed = (input('Soll die Kantenliste als gerichtet betrachtet werden? [y/n]:'))
    a = int(input('Intervall a eingeben: '))
    b = np.inf
    output_file = input_graph.split(".")[0] + '-Ranking' + '.txt'
    G = TemporalGraph()
    if directed == 'y':
        G.import_edgelist(input_graph)
    elif directed == 'n':
        G.import_undirected_edgelist(input_graph)
    G.node_ranking(a, b, output_file)