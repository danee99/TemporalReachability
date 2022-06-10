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

    # prints each node and the corresponding set of outgoing edges of the node
    def print_graph(self):
        for node in range(0, self.n):
            print(str(node) + ": " + str(self.incidence_list[node]))

    # returns the list of the incident edges (sorted by timestamps) for a given node
    def outgoing_edges_from_node(self, node):
        return self.incidence_list[node]

    # returns the out-degree of a node
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
                if u not in self.nodes:
                    self.nodes.append(u)
                if v not in self.nodes:
                    self.nodes.append(v)
                self.incidence_list[u].append((u, v, t, l))

    # calculates for a given source node the earliest arrival times to all other nodes in a time interval [a,b]
    def temporal_earliest_arrival(self, source, a, b):
        earliest_arrival_time = [np.inf for _ in range(self.n)]
        earliest_arrival_time[source] = 0
        PQ = PriorityQueue()
        PQ.put((earliest_arrival_time[source], source))
        while not PQ.empty():
            (current_arrival_time, current_node) = PQ.get()
            for (u, v, t, l) in self.outgoing_edges_from_node(current_node):
                if t < a or t + l > b: continue
                if t + l < earliest_arrival_time[v] and t >= current_arrival_time:
                    earliest_arrival_time[v] = t + l
                    PQ.put((earliest_arrival_time[v], v))
        return earliest_arrival_time

    # calculates for a given node "source" the number of nodes that "source" can reach
    def number_of_reachable_nodes(self, source, a, b):
        reach_set = {source}  # each node can reach itself
        earliest_arrival_time = [np.inf for _ in range(self.n)]
        earliest_arrival_time[source] = 0
        PQ = PriorityQueue()
        PQ.put((earliest_arrival_time[source], source))
        while not PQ.empty():
            (current_arrival_time, current_node) = PQ.get()
            for (u, v, t, l) in self.outgoing_edges_from_node(current_node):
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
                for (u, v, t, l) in self.outgoing_edges_from_node(current_node):
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
                if current_node in visited: continue
                for (u, v, t, l) in self.outgoing_edges_from_node(current_node):
                    if u != x and v != x:
                        if t < a or t + l > b:
                            continue
                        if t + l < earliest_arrival_time[v] and t >= current_arrival_time:
                            reach_set.add(v)
                            earliest_arrival_time[v] = t + l
                            PQ.put((earliest_arrival_time[v], v))
                visited.add(current_node)
            total = total + len(reach_set)
        return 1 - (total / before)

    # node ranking, but with asynchronous multiprocessing
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
    # DATASETS:
    # /edge-lists/wiki_talk_nl.txt          |  |V| = 225.749 | |E| = 1.554.698
    # /edge-lists/wikipediasg.txt           |  |V| = 208.142 | |E| = 810.702
    # /edge-lists/facebook.txt              |  |V| = 63.731  | |E| = 817.035
    # /edge-lists/twitter.txt               |  |V| = 4.605   | |E| = 23.736     352.0 min vs 393.8 min vs 396.1 min
    # /edge-lists/ia-reality-call.txt       |  |V| = 6.809   | |E| = 52.050     307.1 min
    # /edge-lists/infectious.txt            |  |V| = 10.972  | |E| = 415.912    234.7 min vs 230.6 min vs
    # /edge-lists/ia-contacts_dublin.txt    |  |V| = 10.972  | |E| = 415.912    185.7 min
    # /edge-lists/fb-messages.txt           |  |V| = 1.899   | |E| = 61.734     125.2 min
    # /edge-lists/email-dnc.txt             |  |V| = 1.891   | |E| = 39.264     67.23 min
    # /edge-lists/copresence-InVS15.txt     |  |V| = 219     | |E| = 1.283.194  11.76 min
    # /edge-lists/fb-forum.txt              |  |V| = 899     | |E| = 33.720     9.164 min vs 12.03 min vs 12.06 min
    # /edge-lists/tij_SFHH.txt              |  |V| = 403     | |E| = 70.261     5.790 min vs 10.61 min vs 10.25 min
    # /edge-lists/ht09_contact_list.txt     |  |V| = 5.351   | |E| = 20.817     2.727 min vs 2.701 min vs 1.932 min
    # /edge-lists/copresence-InVS13.txt     |  |V| = 95      | |E| = 394.247    0.772 min vs 1.189 min vs 1.235 min
    # reptilia-tortoise-network-fi.txt      |  |V| = 787     | |E| = 1.713      0.053 min
    # /edge-lists/aves-weaver-social.txt    |  |V| = 445     | |E| = 1.426      0.022 min
    # /edge-lists/example_graph1.txt        |  |V| = 7       | |E| = 18         0.005 min
    # /edge-lists/example_graph2.txt        |  |V| = 7       | |E| = 9          0.005 min
