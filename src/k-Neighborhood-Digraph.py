import multiprocessing
import os
from queue import PriorityQueue
import numpy as np
import time

path = os.path.join(os.getcwd(), os.pardir) + "\\edge-lists\\"


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
                if i == k:
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

    def total_reachability_after(self, deleted_node, a, b, k):
        total = 0
        k_neighbours = self.k_neighborhood_subgraph(deleted_node, k)
        before = 0
        for node in k_neighbours:
            reach_set = {node}
            visited = set()
            earliest_arrival_time = {j: np.inf for j in k_neighbours}
            earliest_arrival_time[node] = 0
            PQ = PriorityQueue()
            PQ.put((earliest_arrival_time[node], node))
            while not PQ.empty():
                (current_arrival_time, current_node) = PQ.get()
                if current_node not in visited:
                    for (u, v, t, l) in k_neighbours[current_node]:
                        # for (u, v, t, l) in self.graph[current_node][0]:
                        #     if u not in k_neighbours or v not in k_neighbours: continue
                        if t < a or t + l > b: continue
                        if t + l < earliest_arrival_time[v] and t >= current_arrival_time:
                            reach_set.add(v)
                            earliest_arrival_time[v] = t + l
                            PQ.put((earliest_arrival_time[v], v))
                    visited.add(current_node)
            before += len(reach_set)
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
                    for (u, v, t, l) in k_neighbours[current_node]:
                        # for (u, v, t, l) in self.graph[current_node][0]:
                        #     if u not in k_neighbours or v not in k_neighbours: continue
                        if v != deleted_node and u != deleted_node:
                            if t < a or t + l > b: continue
                            if t + l < earliest_arrival_time[v] and t >= current_arrival_time:
                                reach_set.add(v)
                                earliest_arrival_time[v] = t + l
                                PQ.put((earliest_arrival_time[v], v))
                    visited.add(current_node)
            total += len(reach_set)
        return 1 - (total/before), deleted_node


if __name__ == '__main__':
    input_graph = input('Edgeliste eingeben:')
    k = int(input('k-Nachbarschaft, Gebe den Wert k ein:'))
    directed = (input('Ist der Graph gerichtet? [y/n]:'))
    output_file = input_graph.split(".")[0] + '-k-Nachbarschaft-Ranking (Digraph)' + '.txt'
    G = TemporalGraph()
    G.import_edgelist(input_graph)
    start_time = time.time()
    pool = multiprocessing.Pool(multiprocessing.cpu_count())
    result_objects = [pool.apply_async(G.total_reachability_after, args=(node, 0, np.inf, k)) for node in range(0, G.n)]
    result = [r.get() for r in result_objects]
    pool.close()
    pool.join()
    finish = time.time() - start_time
    with open(path + output_file, 'w') as f:
        # f.write("Avg " + str(int(sum(result) / len(result))) + "\n")
        # f.write("Min " + str(min(result)) + "\n")
        # f.write("Max " + str(max(result)) + "\n")
        result.sort(reverse=True)
        f.write(str(result) + "\n")
        f.write("wurde auf die " + str(k) + "-Nachbarschaft jedes Knotens angewendet." + "\n")
        f.write("|V| = " + str(G.n) + ", |E| = " + str(G.m) + "\n")
        f.write("abgeschlossen in %s Sekunden ---" % finish + "\n")
        f.write("abgeschlossen in %s Minuten ---" % (finish / 60) + "\n")
        f.write("abgeschlossen in %s Stunden ---" % (finish / 3600))
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
