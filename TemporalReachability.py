import multiprocessing
import os
import time
from queue import PriorityQueue
import numpy as np


class TemporalGraph:
    def __init__(self):
        self.nodes = set()
        self.incidence_list = []
        self.n = 0

    # prints each node and the corresponding set of outgoing edges of the node
    def print_graph(self):
        for node in self.nodes:
            print(str(node) + ": " + str(self.incidence_list[node]))

    # returns the outdegree of a node
    def outdegree(self, node):
        return len(self.incidence_list[node])

    # returns a list with every out-degree for each node
    def degree_centrality(self, output_name):
        res = []
        for node in range(0, len(self.nodes)):
            res.append(self.outdegree(node))
        with open(os.getcwd() + output_name, 'w') as f:
            f.write(str(res) + "\n")

    # normalized out-degrees of every node
    def degree_centrality_normalized(self, output_name):
        res = []
        for node in range(0, self.n):
            res.append(self.outdegree(node))
        maximum = max(res)
        minimum = min(res)
        for j in range(0, self.n):
            res[j] = (res[j] - minimum) / (maximum - minimum)
        with open(os.getcwd() + output_name, 'w') as f:
            f.write(str(res) + "\n")

    # scans an edgelist and creates a TemporalGraph object in O(n+m)
    def import_edgelist(self, file_name):
        with open(os.getcwd() + file_name, "r") as f:
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

    # calculates for a given node "source" the number of nodes that "source" can reach
    def number_of_reachable_nodes(self, source, a, b):
        reach_set = {source}  # each node can reach itself
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
    def total_reachability(self, a, b):
        total = 0
        helper = [np.inf for _ in range(self.n)]
        for node in self.nodes:
            reach_set = {node}
            earliest_arrival_time = helper.copy()
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
            total = total + len(reach_set)
        return total

    # ranks a node, where the ranking is a floating point number between 0 and 1
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
            total = total + len(reach_set)
        return 1 - (total / before)

    # node ranking, with asynchronous multiprocessing
    def node_ranking(self, a, b, output_name):
        start_time = time.time()
        before = self.total_reachability(a, b)
        helper = [np.inf for _ in range(self.n)]
        pool = multiprocessing.Pool(multiprocessing.cpu_count())
        result_objects = [pool.apply_async(self.rank_node, args=(node, a, b, before, helper)) for node in
                          range(0, self.n)]
        ranking = [r.get() for r in result_objects]
        pool.close()
        pool.join()
        with open(os.getcwd() + output_name, 'w') as f:
            f.write(str(ranking) + "\n")
            finish = time.time() - start_time
            f.write("--- finished in %s seconds ---" % finish + "\n")
            f.write("--- finished in %s minutes ---" % (finish / 60) + "\n")
            f.write("--- finished in %s hours ---" % (finish / 3600))


if __name__ == '__main__':
    input_graph = '/edge-lists/'+input('Edgeliste eingeben:')
    a = int(input('Intervall a eingeben: '))
    b = np.inf
    output_file = input_graph.split(".")[0] + '-Rangliste' + '.txt'
    degree_output_file = input_graph.split(".")[0] + '-Outdegrees' + '.txt'
    G = TemporalGraph()
    G.import_edgelist(input_graph)
    G.node_ranking(a, b, output_file)
    # DATASETS:                                                                 Node Ranking | Top k | Heuristik 1 | Heuristik 2
    # wiki_talk_nl.txt                      |  |V| = 225.749 | |E| = 1.554.698
    # wikipediasg.txt                       |  |V| = 208.142 | |E| = 810.702
    # facebook.txt                          |  |V| = 63.731  | |E| = 817.035
    # twitter.txt                           |  |V| = 4.605   | |E| = 23.736     352.0 min | 393.8 min | 396.1 min | 33.5 min
    # ia-reality-call.txt                   |  |V| = 6.809   | |E| = 52.050     307.1 min | 343.0 min | xx.xx
    # infectious.txt                        |  |V| = 10.972  | |E| = 415.912    234.7 min | 230.6 min |	xx.xx     | 192.70 min
    # ia-contacts_dublin.txt                |  |V| = 10.972  | |E| = 415.912    185.7 min | 230.5 min | xx.xx
    # fb-messages.txt                       |  |V| = 1.899   | |E| = 61.734     125.2 min | xx.xx min | xx.xx
    # email-dnc.txt                         |  |V| = 1.891   | |E| = 39.264     67.23 min | 66.62 min | 29.14 min
    # copresence-InVS15.txt                 |  |V| = 219     | |E| = 1.283.194  11.76 min | xx.xx min | xx.xx
    # fb-forum.txt                          |  |V| = 899     | |E| = 33.720     9.164 min | 12.03 min | 12.06 min
    # tij_SFHH.txt                          |  |V| = 403     | |E| = 70.261     5.790 min | 10.61 min | 10.25 min
    # ht09_contact_list.txt                 |  |V| = 5.351   | |E| = 20.817     2.727 min | 2.701 min | 1.932 min
    # copresence-InVS13.txt                 |  |V| = 95      | |E| = 394.247    0.771 min | 1.189 min | 1.235 min
    # reptilia-tortoise-network-fi.txt      |  |V| = 787     | |E| = 1.713      0.053 min | 0.036 min | 0.018 min
    # aves-weaver-social.txt                |  |V| = 445     | |E| = 1.426      0.022 min | 0.013 min | 0.008 min
    # example_graph1.txt                    |  |V| = 7       | |E| = 18         0.005 min
    # example_graph2.txt                    |  |V| = 7       | |E| = 9          0.005 min
