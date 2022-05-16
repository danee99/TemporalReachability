import heapq
import multiprocessing
import os
import time
from queue import PriorityQueue
import heapq_max
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
from multiprocessing import Process

result_list = []


def log_result(result):
    result_list.append(result)


class TemporalGraph:
    def __init__(self, nodes, incidence_list):
        self.nodes = []
        self.incidence_list = []

    # prints the set of nodes and the corresponding incidence list
    def print_graph(self):
        for node in self.nodes:
            print(str(node) + ": " + str(self.incidence_list[node]))

    # returns the list of the incident edges (sorted by timestamps) for a given node
    def edges_of_node(self, node):
        return self.incidence_list[node]

    # returns the out-degree of a node
    def outdegree(self, node):
        return len(self.incidence_list[node])

    # scans the edgelist and adds all nodes and edges to the Graph
    # Graph is created in O(n+m)
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

    # calculates for a given source node the earliest arrival times to all other nodes in an interval [a,b]
    def temporal_earliest_arrival(self, source, a, b):
        # reach_set = [source]
        earliest_arrival_time = [np.inf for _ in range(len(self.nodes))]
        earliest_arrival_time[source] = 0
        PQ = PriorityQueue()
        PQ.put((earliest_arrival_time[source], source))
        visited = []
        while not PQ.empty():
            # print("Prioritätswarteschlange: " + str(PQ.queue))
            (current_arrival_time, current_node) = PQ.get()
            if current_node not in visited:
                for (u, v, t, l) in self.edges_of_node(current_node):
                    if t < a or t + l > b: continue
                    if t + l < earliest_arrival_time[v] and t >= earliest_arrival_time[u]:
                        # if v not in reach_set:
                        #     reach_set.append(v)
                        earliest_arrival_time[v] = t + l
                        PQ.put((earliest_arrival_time[v], v))
                visited.append(current_node)
        # return len(reach_set)
        return earliest_arrival_time

    # calculates for a given node "source" the number of nodes that "source" can reach
    def number_of_reachable_nodes(self, source, a, b):
        # source can reach itself
        reach_set = [source]
        earliest_arrival_time = [np.inf for _ in range(len(self.nodes))]
        earliest_arrival_time[source] = 0
        PQ = PriorityQueue()
        PQ.put((earliest_arrival_time[source], source))
        visited = []
        while not PQ.empty():
            (current_arrival_time, current_node) = PQ.get()
            if current_node not in visited:
                for (u, v, t, l) in self.edges_of_node(current_node):
                    if t < a or t + l > b: continue
                    if t + l < earliest_arrival_time[v] and t >= earliest_arrival_time[u]:
                        if v not in reach_set:
                            reach_set.append(v)
                        earliest_arrival_time[v] = t + l
                        PQ.put((earliest_arrival_time[v], v))
                visited.append(current_node)
        return len(reach_set)

    # calculates the total reachability of the given graph in a time interval [a,b]
    def total_reachability(self, a, b):
        total = []
        helper = [np.inf for _ in range(len(self.nodes))]
        for node in self.nodes:
            reach_set = [node]
            earliest_arrival_time = helper[:]
            earliest_arrival_time[node] = 0
            PQ = PriorityQueue()
            PQ.put((earliest_arrival_time[node], node))
            # visited = []
            while not PQ.empty():
                (current_arrival_time, current_node) = PQ.get()
                # if current_node not in visited:
                for (u, v, t, l) in self.edges_of_node(current_node):
                    if t < a or t + l > b: continue
                    if t + l < earliest_arrival_time[v] and t >= earliest_arrival_time[u]:
                        if v not in reach_set:
                            reach_set.append(v)
                        earliest_arrival_time[v] = t + l
                        PQ.put((earliest_arrival_time[v], v))
                # visited.append(current_node)
            total.append(len(reach_set))
        return sum(total)

    # calculates the total reachability of a given graph in a time interval [a,b] after deleting a node x
    def total_reachability_after(self, x, a, b, helper):
        total = []
        for node in self.nodes:
            if node == x:
                continue
            reach_set = [node]
            earliest_arrival_time = helper.copy()
            earliest_arrival_time[node] = 0
            PQ = PriorityQueue()
            PQ.put((earliest_arrival_time[node], node))
            while not PQ.empty():
                (current_arrival_time, current_node) = PQ.get()
                for (u, v, t, l) in self.edges_of_node(current_node):
                    if u != x and v != x:
                        if t < a or t + l > b:
                            continue
                        if t + l < earliest_arrival_time[v] and t >= earliest_arrival_time[u]:
                            if v not in reach_set:
                                reach_set.append(v)
                            earliest_arrival_time[v] = t + l
                            PQ.put((earliest_arrival_time[v], v))
            total.append(len(reach_set))
        return sum(total)

    # calculates the total reachability of a given graph in a time interval [a,b] after deleting a node x
    def rank_node(self, x, a, b, helper, before):
        total = []
        for node in self.nodes:
            if node == x:
                continue
            reach_set = [node]
            earliest_arrival_time = helper.copy()
            earliest_arrival_time[node] = 0
            PQ = PriorityQueue()
            PQ.put((earliest_arrival_time[node], node))
            while not PQ.empty():
                (current_arrival_time, current_node) = PQ.get()
                for (u, v, t, l) in self.edges_of_node(current_node):
                    if u != x and v != x:
                        if t < a or t + l > b:
                            continue
                        if t + l < earliest_arrival_time[v] and t >= earliest_arrival_time[u]:
                            if v not in reach_set:
                                reach_set.append(v)
                            earliest_arrival_time[v] = t + l
                            PQ.put((earliest_arrival_time[v], v))
            total.append(len(reach_set))
        return 1 - (sum(total) / before)

    # returns node ranking
    def node_ranking(self, a, b):
        start_time = time.time()
        before = self.total_reachability(a, b)
        helper = [np.inf for _ in range(len(self.nodes))]
        result = []
        for node in range(0, len(self.nodes)):
            result.append(self.rank_node(node, a, b, helper, before))
        finish = time.time() - start_time
        print(finish)
        return result

    def fast_node_ranking(self, a, b, output_name):
        start_time = time.time()
        before = self.total_reachability(a, b)
        helper = [np.inf for _ in range(len(self.nodes))]
        pool = multiprocessing.Pool(multiprocessing.cpu_count())
        for node in self.nodes:
            pool.apply_async(self.rank_node, args=(node, a, b, helper, before), callback=log_result)
        pool.close()
        pool.join()
        with open(os.getcwd() + output_name, 'w') as f:
            f.write(str(result_list) + "\n")
            # top3 = heapq.nlargest(7, result_list)
            # for i in top3:
            #     f.write(str((result_list.index(i), i)) + "\n")
            finish = time.time() - start_time
            f.write("--- finished in %s seconds ---" % (finish) + "\n")
            f.write("--- finished in %s minutes ---" % ((finish) / 60) + "\n")
            f.write("--- finished in %s hours ---" % ((finish) / 3600))
        # return result_list


if __name__ == '__main__':
    input_graph = input('Edgeliste eingeben: ')
    output_file = input_graph.split(".")[0] + '-RANKING' + '.txt'
    G = TemporalGraph([], [])
    G.import_edgelist(input_graph)
    G.fast_node_ranking(0, np.inf, output_file)
    # /edge-lists/wiki_talk_nl            |  V = 225749 | E = 1554698
    # /edge-lists/wikipediasg.txt         |  V = 208142 | E = 810702
    # /edge-lists/facebook.txt            |  V = 63731  | E = 817036
    # /edge-lists/infectious.txt          |  V = 10972  | E = 415912
    # /edge-lists/tij_SFHH.txt            |  V = 3906   | E = 70261
    # /edge-lists/ht09_contact_list.txt   |  V = 5351   | E = 20817
    # /edge-lists/aves-weaver-social.txt  |  V = 445    | E = 1426
    # /edge-lists/test.txt                |  V = 7      | E = 18
    # /edge-lists/comparison.txt          |  V = 7      | E = 9
