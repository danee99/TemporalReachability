import multiprocessing
import os
import time
from queue import PriorityQueue
import numpy as np

path = os.path.join(os.getcwd(), os.pardir) + "\\edge-lists\\"


class TemporalGraph:
    def __init__(self):
        self.n = 0
        self.m = 0
        self.graph = {}
        self.reachability_change_of_deleted_nodes = 0
        self.num_deleted_nodes = 0

    def add_edge(self, u, v, t, l):
        if u not in self.graph:
            self.graph[u] = [[(u, v, t, l)], 1, 0]
        else:
            if v not in [self.graph[u][0][i][1] for i in range(0, len(self.graph[u][0]))]:
                self.graph[u][1] += 1
            self.graph[u][0].append((u, v, t, l))
        if v not in self.graph:
            self.graph[v] = [[], 0, 0]
        self.m += 1

    def print_graph(self):
        print("|V| = " + str(self.n))
        print("|E| = " + str(self.m))
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

    def max_degree(self):
        var = [self.graph[u][1] for u in self.graph]
        print(int(sum(var) / len(var)))
        print(int(min(var)))
        print(int(max(var)))

    def degree_centrality(self, output_name):
        res = []
        for node in range(0, self.n):
            res.append(self.graph[node][1])
        with open(path + output_name, 'w') as f:
            f.write(str(res))

    def filter_nodes(self, depth):
        # Problem 1: Erreichbarkeiten der In-Nachbarn der gelöschten Knoten speichern
        # Problem 2: Erreichbarkeiten der gelöschten Knoten speichern
        # Problem 3: Erreichbarkeiten von x fallen bei der Berechnung von R(G-x) weg
        deleted_nodes = []
        for i in range(0, depth):
            for node in self.graph:
                if self.graph[node][1] == 0:
                    deleted_nodes.append(node)
                    self.num_deleted_nodes += 1
                    self.graph[node][2] += 1
            for node in self.graph:
                visited = set()
                for (u, v, t, l) in self.graph[node][0][:]:
                    if v in deleted_nodes:
                        if v not in visited:  # because of multi edges
                            self.graph[node][2] += 1
                            self.graph[node][1] -= 1
                        self.graph[u][0].remove((u, v, t, l))
                        self.m -= 1
                        visited.add(v)
            while deleted_nodes:
                delete_me = deleted_nodes.pop(0)
                self.reachability_change_of_deleted_nodes += self.graph[delete_me][2]
                try:
                    del self.graph[delete_me]
                    self.n -= 1
                except KeyError:
                    continue

    def calculate_bounds(self, a, b, x):
        lower_bound = self.reachability_change_of_deleted_nodes
        upper_bound = self.reachability_change_of_deleted_nodes
        for node in self.graph:
            if node == x:
                continue
            reach_set = {node}
            visited = set()
            earliest_arrival_time = {v: np.inf for v in self.graph}
            earliest_arrival_time[node] = 0
            PQ = PriorityQueue()
            PQ.put((earliest_arrival_time[node], node))
            while not PQ.empty():
                (current_arrival_time, current_node) = PQ.get()
                if current_node not in visited:
                    for (u, v, t, l) in self.graph[current_node][0]:
                        if u != x and v != x:
                            if t < a or t + l > b: continue
                            if t + l < earliest_arrival_time[v] and t >= current_arrival_time:
                                reach_set.add(v)
                                earliest_arrival_time[v] = t + l
                                PQ.put((earliest_arrival_time[v], v))
                    visited.add(current_node)
            lower_bound += len(reach_set) + self.graph[node][2]
            upper_bound += len(reach_set) + self.num_deleted_nodes
        return x, (lower_bound, upper_bound)

    def heuristik(self, a, b, output_name, depth):
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
            ranking.sort(key=lambda tup: tup[1][0])
            f.write(str(ranking) + "\n")
            f.write("mit Tiefe = " + str(depth) + "\n")
            f.write("geloeschte Knotenanzahl = " + str(num_nodes - self.n) + "\n")
            f.write("geloeschte Kanten = " + str(num_edges - self.m) + "\n")
            f.write("filter_nodes() abgeschlossen in %s Sekunden" % finish1 + "\n")
            f.write("abgeschlossen in %s Sekunden" % finish2 + "\n")
            f.write("abgeschlossen in %s Minuten" % (finish2 / 60) + "\n")
            f.write("abgeschlossen in %s Stunden" % (finish2 / 3600))
    # def heuristik(self, a, b, output_name, depth):
    #     num_edges = self.m
    #     num_nodes = self.n
    #     start_time = time.time()
    #     self.filter_nodes(depth)
    #     finish1 = time.time() - start_time
    #     ranking = []
    #     for node in self.graph:
    #         ranking.append(self.calculate_bounds(a, b, node))
    #     finish2 = time.time() - start_time
    #     with open(path + output_name, 'w') as f:
    #         ranking.sort(key=lambda tup: tup[1][0])
    #         f.write(str(ranking) + "\n")
    #         f.write("mit Tiefe = " + str(depth) + "\n")
    #         f.write("geloeschte Knotenanzahl = " + str(num_nodes - self.n) + "\n")
    #         f.write("geloeschte Kanten = " + str(num_edges - self.m) + "\n")
    #         f.write("filter_nodes() abgeschlossen in %s Sekunden" % finish1 + "\n")
    #         f.write("abgeschlossen in %s Sekunden" % finish2 + "\n")
    #         f.write("abgeschlossen in %s Minuten" % (finish2 / 60) + "\n")
    #         f.write("abgeschlossen in %s Stunden" % (finish2 / 3600))


if __name__ == '__main__':
    input_graph = input('Edgeliste eingeben:')
    directed = (input('Ist der Graph gerichtet? [y/n]:'))
    depth = int(input('Tiefe eingeben:'))
    degree_output_file = input_graph.split(".")[0] + '-Outdegrees' + '.txt'
    heuristik_output_file = input_graph.split(".")[0] + '-Heuristik' + '.txt'
    ranking_output_file = input_graph.split(".")[0] + '-Rangliste' + '.txt'
    G = TemporalGraph()
    if directed == 'y':
        G.import_edgelist(input_graph)
    elif directed == 'n':
        G.import_undirected_edgelist(input_graph)
    G.heuristik(0, np.inf, heuristik_output_file, depth)
    # DATASETS:                                     Node Ranking                        für gerichteten Graph
    # wiki_talk_nl.txt                              |  |V| = 225.749 | |E| = 1.554.698
    # wikipediasg.txt                               |  |V| = 208.142 | |E| = 810.702
    # facebook.txt                                  |  |V| = 63.731  | |E| = 817.035
    # twitter.txt                                   |  |V| = 4.605   | |E| = 23.736     167 min
    # ia-reality-call.txt (Undirected)              |  |V| = 6.809   | |E| = 52.050     137 min
    # infectious.txt (Undirected ?)                 |  |V| = 10.972  | |E| = 415.912    130 min
    # ia-contacts_dublin.txt (Undirected)           |  |V| = 10.972  | |E| = 415.912    xxx min
    # fb-messages.txt (Directed)                    |  |V| = 1.899   | |E| = 61.734     47 min
    # UC-Irvine-messages.txt (Directed)             |  |V| = 1.899   | |E| = 59.385     47 min
    # High-School_data_2013.txt (Undirected)        |  |V| = 327     | |E| = 59.385
    # email-dnc.txt (Directed)                      |  |V| = 1.891   | |E| = 39.264     13 min
    # copresence-InVS15.txt (Undirected)            |  |V| = 219     | |E| = 1.283.194  7 min
    # ht09_contact_list.txt (Undirected)            |  |V| = 5.351   | |E| = 20.817     4 min
    # fb-forum.txt (directed)                       |  |V| = 899     | |E| = 33.720     3 min
    # tij_SFHH.txt (Undirected)                     |  |V| = 403     | |E| = 70.261     2 min
    # copresence-InVS13.txt (Undirected ?)          |  |V| = 95      | |E| = 394.247    1 min
    # reptilia-tortoise-network-fi.txt (Undirected) |  |V| = 787     | |E| = 1.713      0 min
    # aves-weaver-social.txt (Undirected)           |  |V| = 445     | |E| = 1.426      0 min
    # example_graph1.txt                            |  |V| = 7       | |E| = 18
    # example_graph2.txt                            |  |V| = 7       | |E| = 9
