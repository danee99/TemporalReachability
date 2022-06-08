import multiprocessing
import os
import time
from queue import PriorityQueue
import numpy as np


class TemporalGraph:
    def __init__(self):
        self.nodes = []
        self.incidence_list = []
        self.n = 0
        self.outdegree = []

    # prints each node and the corresponding set of outgoing edges of the node
    def print_graph(self):
        for node in range(0, self.n):
            print(str(node) + ": " + str(self.incidence_list[node]))

    # returns the out-degree of a node
    def outdegree(self, node):
        return len(self.incidence_list[node])

    # scans an edgelist and creates a TemporalGraph object in O(n+m)
    def import_edgelist(self, file_name):
        with open(os.getcwd() + file_name, "r") as f:
            n = int(f.readline())
            self.n = n
            self.incidence_list = [[] for _ in range(n)]
            self.outdegree = [0 for _ in range(n)]
            for line in f:
                arr = line.split()
                u = int(arr[0])
                v = int(arr[1])
                t = int(arr[2])
                try:
                    l = int(arr[3])
                except IndexError:
                    l = 1
                if u not in self.nodes:
                    self.nodes.append(u)
                if v not in self.nodes:
                    self.nodes.append(v)
                self.outdegree[u] = self.outdegree[u] + 1
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
                print(u, v, t, l)
                if t < a or t + l > b: continue
                if t + l < earliest_arrival_time[v] and t >= current_arrival_time:
                    reach_set.add(v)
                    earliest_arrival_time[v] = t + l
                    PQ.put((earliest_arrival_time[v], v))
        return len(reach_set)


if __name__ == '__main__':
    input_graph = '/edge-lists/complete.txt'
    a = 0
    b = np.inf
    output_file = input_graph.split(".")[0] + '-Rangliste2' + '.txt'
    degree_output_file = input_graph.split(".")[0] + '-Outdegrees' + '.txt'
    G = TemporalGraph()
    G.import_edgelist(input_graph)
    print(G.number_of_reachable_nodes(9, a, b))
    G.print_graph()
    # DATASETS:
    # /edge-lists/wiki_talk_nl.txt          |  |V| = 225.749 | |E| = 1.554.698
    # /edge-lists/wikipediasg.txt           |  |V| = 208.142 | |E| = 810.702
    # /edge-lists/facebook.txt              |  |V| = 63.731  | |E| = 817.035
    # /edge-lists/twitter.txt               |  |V| = 4.605   | |E| = 23.736     352.0 min vs 393.8 min
    # /edge-lists/ia-reality-call.txt       |  |V| = 6.809   | |E| = 52.050     307.1 min vs 343.8 min
    # /edge-lists/infectious.txt            |  |V| = 10.972  | |E| = 415.912    234.7 min vs 230.6 min
    # /edge-lists/ia-contacts_dublin.txt    |  |V| = 10.972  | |E| = 415.912    185.7 min
    # /edge-lists/fb-messages.txt           |  |V| = 1.899   | |E| = 61.734     125.2 min
    # /edge-lists/email-dnc.txt             |  |V| = 1.891   | |E| = 39.264     67.23 min
    # /edge-lists/copresence-InVS15.txt     |  |V| = 219     | |E| = 1.283.194  11.76 min
    # /edge-lists/fb-forum.txt              |  |V| = 899     | |E| = 33.720     9.164 min
    # /edge-lists/tij_SFHH.txt              |  |V| = 403     | |E| = 70.261     5.790 min
    # /edge-lists/ht09_contact_list.txt     |  |V| = 5.351   | |E| = 20.817     2.727 min
    # /edge-lists/copresence-InVS13.txt     |  |V| = 95      | |E| = 394.247    0.772 min
    # reptilia-tortoise-network-fi.txt      |  |V| = 787     | |E| = 1.713      0.053 min
    # /edge-lists/aves-weaver-social.txt    |  |V| = 445     | |E| = 1.426      0.022 min
    # /edge-lists/example_graph1.txt        |  |V| = 7       | |E| = 18         0.005 min
    # /edge-lists/example_graph2.txt        |  |V| = 7       | |E| = 9          0.005 min
