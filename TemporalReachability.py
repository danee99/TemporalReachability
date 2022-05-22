import heapq
import multiprocessing
import time
from queue import PriorityQueue
import heapq_max
import numpy as np
import os

result_list = []


def log_result(result):
    result_list.append(result)


class TemporalGraph:
    def __init__(self):
        self.nodes = []
        self.incidence_list = []

    # prints each node and the corresponding set of outgoing edges of the node
    def print_graph(self):
        for node in self.nodes:
            print(str(node) + ": " + str(self.incidence_list[node]))

    # returns the list of the incident edges (sorted by timestamps) for a given node
    def outgoing_edges_from_node(self, node):
        return self.incidence_list[node]

    # returns the out-degree of a node
    def outdegree(self, node):
        return len(self.incidence_list[node])

    # returns the out-degree of a node
    def degree_centrality(self):
        res = []
        for node in range(0, len(self.nodes)):
            res.append(self.outdegree(node))
        maximum = max(res)
        for i in range(0, len(self.nodes)):
            res[i] = res[i]/maximum
        return res

    # scans an edgelist and creates a TemporalGraph object in O(n+m)
    def import_edgelist(self, file_name):
        with open(os.getcwd() + file_name, "r") as f:
            self.incidence_list = [[] for _ in range(int(f.readline()))]
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
        earliest_arrival_time = [np.inf for _ in range(len(self.nodes))]
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
        # each node can reach itself
        reach_set = {source}
        earliest_arrival_time = [np.inf for _ in range(len(self.nodes))]
        earliest_arrival_time[source] = 0
        PQ = PriorityQueue()
        PQ.put((earliest_arrival_time[source], source))
        while not PQ.empty():
            (current_arrival_time, current_node) = PQ.get()
            for (u, v, t, l) in self.outgoing_edges_from_node(current_node):
                if t < a or t + l > b: continue
                if t + l < earliest_arrival_time[v] and t >= earliest_arrival_time[u]:
                    reach_set.add(v)
                    earliest_arrival_time[v] = t + l
                    PQ.put((earliest_arrival_time[v], v))
        return len(reach_set)

    # calculates the total reachability of the given temporal graph in a time interval [a,b]
    def total_reachability(self, a, b):
        total = 0
        helper = [np.inf for _ in range(len(self.nodes))]
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
                    if t + l < earliest_arrival_time[v] and t >= earliest_arrival_time[u]:
                        reach_set.add(v)
                        earliest_arrival_time[v] = t + l
                        PQ.put((earliest_arrival_time[v], v))
            total = total + len(reach_set)
        return total

    # calculates the total reachability of a given graph in a time interval [a,b] after deleting the node "x"
    def total_reachability_after(self, x, a, b, helper):
        total = 0
        for node in self.nodes:
            if node == x:
                continue
            reach_set = {node}
            earliest_arrival_time = helper.copy()
            earliest_arrival_time[node] = 0
            PQ = PriorityQueue()
            PQ.put((earliest_arrival_time[node], node))
            while not PQ.empty():
                (current_arrival_time, current_node) = PQ.get()
                for (u, v, t, l) in self.outgoing_edges_from_node(current_node):
                    if u != x and v != x:
                        if t < a or t + l > b:
                            continue
                        if t + l < earliest_arrival_time[v] and t >= current_arrival_time:
                            reach_set.add(v)
                            earliest_arrival_time[v] = t + l
                            PQ.put((earliest_arrival_time[v], v))
            total = total + len(reach_set)
        return total

    # ranks a node, where the ranking is a floating point number between 0 and 1
    def rank_node(self, x, a, b, before, helper):
        after = self.total_reachability_after(x, a, b, helper)
        return 1 - (after / before), x

    # returns array with rank of every node
    def node_ranking(self, a, b):
        before = self.total_reachability(a, b)
        helper = [np.inf for _ in range(len(self.nodes))]
        ranking = []
        for node in range(0, len(self.nodes)):
            ranking.append(self.rank_node(node, a, b, before, helper))
        print(ranking)

    # node ranking but with multiprocessing
    def fast_node_ranking(self, a, b, output_name):
        start_time = time.time()
        before = self.total_reachability(a, b)
        helper = [np.inf for _ in range(len(self.nodes))]
        pool = multiprocessing.Pool(multiprocessing.cpu_count())
        ranking = [pool.apply(self.rank_node, args=(node, a, b, before, helper)) for node in self.nodes]
        pool.close()
        with open(os.getcwd() + output_name, 'w') as f:
            f.write(str(ranking) + "\n")
            finish = time.time() - start_time
            f.write("--- finished in %s seconds ---" % (finish) + "\n")
            f.write("--- finished in %s minutes ---" % ((finish) / 60) + "\n")
            f.write("--- finished in %s hours ---" % ((finish) / 3600))

    # alternative node ranking, but with asynchronous multiprocessing
    def alternative_node_ranking(self, a, b, output_name):
        start_time = time.time()
        before = self.total_reachability(a, b)
        helper = [np.inf for _ in range(len(self.nodes))]
        pool = multiprocessing.Pool(multiprocessing.cpu_count())
        for node in self.nodes:
            pool.apply_async(self.rank_node, args=(node, a, b, before, helper), callback=log_result)
        pool.close()
        pool.join()
        result_list.sort(key=lambda tup: tup[1])
        with open(os.getcwd() + output_name, 'w') as f:
            f.write(str([x[0] for x in result_list]) + "\n")
            finish = time.time() - start_time
            f.write("--- finished in %s seconds ---" % (finish) + "\n")
            f.write("--- finished in %s minutes ---" % ((finish) / 60) + "\n")
            f.write("--- finished in %s hours ---" % ((finish) / 3600))


if __name__ == '__main__':
    input_graph = input('Edgeliste eingeben: ')
    a = int(input('Intervall a eingeben: '))
    # b = int(input('Intervall b eingeben: '))
    b = np.inf
    output_file = input_graph.split(".")[0] + '-RANKING2' + '.txt'
    G = TemporalGraph()
    G.import_edgelist(input_graph)
    G.fast_node_ranking(a, b, output_file)
    # DATASETS:
    # /edge-lists/wiki_talk_nl.txt          |  |V| = 225.749 | |E| = 1.554.698
    # /edge-lists/wikipediasg.txt           |  |V| = 208.142 | |E| = 810.702
    # /edge-lists/facebook.txt              |  |V| = 63.731  | |E| = 817.035
    # /edge-lists/infectious.txt            |  |V| = 10.972  | |E| = 415.912
    # /edge-lists/ht09_contact_list.txt     |  |V| = 5.351   | |E| = 20.817
    # /edge-lists/tij_SFHH.txt              |  |V| = 3.906   | |E| = 70.261
    # /edge-lists/twitter.txt               |  |V| = 4.605   | |E| = 23.736
    # /edge-lists/email-dnc.txt             |  |V| = 1.891   | |E| = 39.264
    # /edge-lists/aves-weaver-social.txt    |  |V| = 445     | |E| = 1.426
    # /edge-lists/example_graph1.txt        |  |V| = 7       | |E| = 18
    # /edge-lists/example_graph2.txt        |  |V| = 7       | |E| = 9