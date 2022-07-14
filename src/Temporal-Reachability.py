import multiprocessing
import os
import time
from queue import PriorityQueue
import numpy as np

path = os.path.join(os.getcwd(), os.pardir) + "\\edge-lists\\"


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
        reach_set = {source}
        earliest_arrival_time = [np.inf for _ in range(self.n)]
        earliest_arrival_time[source] = 0
        PQ = PriorityQueue()
        PQ.put((earliest_arrival_time[source], source))
        while not PQ.empty():
            (current_arrival_time, current_node) = PQ.get()
            for (u, v, t, l) in self.incidence_list[current_node]:
                if t < a or t + l > b: continue
                if t + l < earliest_arrival_time[v] and t >= current_arrival_time:
                    reach_set.add(v)
                    earliest_arrival_time[v] = t + l
                    PQ.put((earliest_arrival_time[v], v))
        return len(reach_set)

    # calculates the total reachability of the given temporal graph in a time interval [a,b]
    def calc_total_reachability(self, a, b):
        for node in self.nodes:
            reach_set = {node}
            earliest_arrival_time = [np.inf for _ in range(self.n)]
            earliest_arrival_time[node] = 0
            PQ = PriorityQueue()
            PQ.put((earliest_arrival_time[node], node))
            while not PQ.empty():
                (current_arrival_time, current_node) = PQ.get()
                for (u, v, t, l) in self.incidence_list[current_node]:
                    if t < a or t + l > b: continue
                    if t + l < earliest_arrival_time[v] and t >= current_arrival_time:
                        reach_set.add(v)
                        earliest_arrival_time[v] = t + l
                        PQ.put((earliest_arrival_time[v], v))
            self.total_reachability += len(reach_set)

    # ranks the node "x", where the ranking is a floating point number between 0 and 1
    def rank_node(self, x, a, b, before, helper):
        total = 0
        for node in self.nodes:
            if node == x:
                continue
            reach_set = {node}
            visited = set()
            earliest_arrival_time = helper.copy()
            earliest_arrival_time[node] = 0
            PQ = PriorityQueue()
            PQ.put((earliest_arrival_time[node], node))
            while not PQ.empty():
                (current_arrival_time, current_node) = PQ.get()
                if current_node not in visited:
                    for (u, v, t, l) in self.incidence_list[current_node]:
                        if u != x and v != x:
                            if t < a or t + l > b: continue
                            if t + l < earliest_arrival_time[v] and t >= current_arrival_time:
                                reach_set.add(v)
                                earliest_arrival_time[v] = t + l
                                PQ.put((earliest_arrival_time[v], v))
                    visited.add(current_node)
            total += len(reach_set)
        return 1 - (total / before)

    # parallelized node ranking
    def node_ranking(self, a, b, output_name):
        start_time = time.time()
        self.calc_total_reachability(a, b)
        helper = [np.inf for _ in range(self.n)]
        pool = multiprocessing.Pool(multiprocessing.cpu_count())
        result_objects = [pool.apply_async(self.rank_node, args=(node, a, b, self.total_reachability, helper)) for node
                          in range(0, self.n)]
        ranking = [r.get() for r in result_objects]
        pool.close()
        pool.join()
        finish = time.time() - start_time
        with open(path + output_name, 'w') as f:
            f.write(str(ranking) + "\n")
            f.write("abgeschlossen in %s Sekunden" % finish + "\n")
            f.write("abgeschlossen in %s Minuten" % (finish / 60) + "\n")
            f.write("abgeschlossen in %s Stunden" % (finish / 3600))

    def DFS(self, v, visited):
        visited[v] = True
        for (v, u, t, l) in self.incidence_list[v]:
            if not visited[u]:
                self.DFS(u, visited)

    def is_Connected(self):
        for i in range(self.n):
            visited = [False] * self.n
            self.DFS(i, visited)
            for b in visited:
                if not b:
                    return False
        return True


if __name__ == '__main__':
    input_graph = input('Edgeliste eingeben:')
    directed = (input('Ist der Graph gerichtet? [y/n]:'))
    a = int(input('Intervall a eingeben: '))
    b = np.inf
    output_file = input_graph.split(".")[0] + '-Ranking' + '.txt'
    G = TemporalGraph()
    if directed == 'y':
        G.import_edgelist(input_graph)
    elif directed == 'n':
        G.import_undirected_edgelist(input_graph)
    # G.node_ranking(a, b, output_file)
    if G.is_Connected():
        print('Der Graph ist stark verbunden')
    else:
        print('Der Graph ist nicht stark verbunden')
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
