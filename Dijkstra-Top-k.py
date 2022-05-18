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
    heapq.heappush(result_list, result)


class TemporalGraph:
    def __init__(self, nodes, incidence_list):
        self.nodes = []
        self.incidence_list = []

    # outputs the set of nodes and the incidence list
    def print_graph(self):
        print(self.nodes)
        print(self.incidence_list)

    # returns the list of the incident edges (sorted by timestamps) for a given node
    def edges_of_node(self, node):
        return self.incidence_list[node]

    # scans the edgelist and adds all nodes and edges to the Graph
    # Graph is created in O(m) because all edges are iterated through
    def import_edgelist(self, file_name):
        with open(os.getcwd() + file_name, "r") as f:
            n = int(f.readline())
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

    # calculates for a given source node the earliest arrival times to all other nodes
    def temporal_earliest_arrival(self, source):
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
                    if t + l < earliest_arrival_time[v] and t >= earliest_arrival_time[u]:
                        earliest_arrival_time[v] = t + l
                        PQ.put((earliest_arrival_time[v], v))
                visited.append(current_node)
        return len([x for x in earliest_arrival_time if x != np.inf])

    def total_reach(self, a, b):
        total = 0
        help_list = [np.inf for _ in range(len(self.nodes))]
        for node in self.nodes:
            reach_num = 1
            earliest_arrival_time = help_list.copy()
            earliest_arrival_time[node] = 0
            PQ = PriorityQueue()
            PQ.put((earliest_arrival_time[node], node))
            visited = []
            while not PQ.empty():
                (current_arrival_time, current_node) = PQ.get()
                for (u, v, t, l) in self.edges_of_node(current_node):
                    if t < a or t + l > b:
                        continue
                    if t + l < earliest_arrival_time[v] and t >= earliest_arrival_time[u] and v not in visited:
                        visited.append(v)
                        reach_num = reach_num + 1
                        earliest_arrival_time[v] = t + l
                        PQ.put((earliest_arrival_time[v], v))
            total = total + reach_num
        # return total, x
        return total

    def top_k_util(self, a, b, x, helper):
        total = 0
        for node in self.nodes:
            reach_num = 1
            if node == x:
                continue
            earliest_arrival_time = helper.copy()
            earliest_arrival_time[node] = 0
            PQ = PriorityQueue()
            PQ.put((earliest_arrival_time[node], node))
            visited = [x]
            while not PQ.empty():
                (current_arrival_time, current_node) = PQ.get()
                if current_node != x:
                    for (u, v, t, l) in self.edges_of_node(current_node):
                        if u != x and v != x:
                            if t < a or t + l > b:
                                continue
                            if t + l < earliest_arrival_time[v] and t >= earliest_arrival_time[u] and v not in visited:
                                visited.append(v)
                                reach_num = reach_num + 1
                                earliest_arrival_time[v] = t + l
                                PQ.put((earliest_arrival_time[v], v))
            total = total + reach_num
        # return total, x
        return total

    def top_k_nodes(self, alpha, beta, k, output_file):
        start_time = time.time()
        help_list = [np.inf for _ in range(len(self.nodes))]
        pool = multiprocessing.Pool(multiprocessing.cpu_count())
        for node in self.nodes:
            pool.apply_async(self.top_k_util, args=(alpha, beta, node, help_list), callback=log_result)
        pool.close()
        pool.join()
        with open(os.getcwd() + output_file, 'w') as f:
            f.write(str(heapq.nsmallest(k, result_list)) + "\n")
            finish = time.time() - start_time
            f.write("--- finished in %s seconds ---" % (finish) + "\n")
            f.write("--- finished in %s minutes ---" % ((finish) / 60) + "\n")
            f.write("--- finished in %s hours ---" % ((finish) / 3600))

    def node_ranking(self, alpha, beta, k, output_file):
        start_time = time.time()
        before = self.total_reach(0, np.inf)
        ranks = []
        help_list = [np.inf for _ in range(len(self.nodes))]
        for node in self.nodes:
            ranks.append(1-(self.top_k_util(alpha, beta, node, help_list)/before))
        with open(os.getcwd() + output_file, 'w') as f:
            f.write(str(ranks) + "\n")
            finish = time.time() - start_time
            f.write("--- finished in %s seconds ---" % (finish) + "\n")
            f.write("--- finished in %s minutes ---" % ((finish) / 60) + "\n")
            f.write("--- finished in %s hours ---" % ((finish) / 3600))

    def inner(self, a, b, x, max_heap, k, helper):
        total = 0
        for node in self.nodes:
            reach_num = 1
            if node == x:
                continue
            earliest_arrival_time = helper.copy()
            earliest_arrival_time[node] = 0
            PQ = PriorityQueue()
            PQ.put((earliest_arrival_time[node], node))
            visited = [x]
            while not PQ.empty():
                (current_arrival_time, current_node) = PQ.get()
                if current_node != x:
                    for (u, v, t, l) in self.edges_of_node(current_node):
                        if u != x and v != x:
                            if t < a or t + l > b:
                                continue
                            if t + l < earliest_arrival_time[v] and t >= earliest_arrival_time[u] and v not in visited:
                                visited.append(v)
                                reach_num = reach_num + 1
                                earliest_arrival_time[v] = t + l
                                PQ.put((earliest_arrival_time[v], v))
            total = total + reach_num
            if max_heap != [] and len(max_heap) >= k:
                if total > max_heap[0][0]:
                    return
        if len(max_heap) < k:
            heapq_max.heappush_max(max_heap, (total, x))
        else:
            if total < max_heap[0][0]:
                heapq_max.heappushpop_max(max_heap, (total, x))

    # outputs the top k nodes
    def outer(self, a, b, k, output_name):
        start_time = time.time()
        max_heap = []
        help_list = [np.inf for i in range(0, len(self.nodes))]
        for node in self.nodes:
            self.inner(a, b, node, max_heap, k, help_list)
        with open(os.getcwd() + output_name, 'w') as f:
            f.write(str(max_heap) + "\n")
            finish = time.time() - start_time
            f.write("--- finished in %s seconds ---" % (finish) + "\n")
            f.write("--- finished in %s minutes ---" % ((finish) / 60) + "\n")
            f.write("--- finished in %s hours ---" % ((finish) / 3600))


# using the networkx library to plot the graph in a more appealing way
def draw_graph(file_name):
    G = nx.Graph()
    file = os.getcwd() + file_name
    with open(file, "r") as f:
        n = int(f.readline())
        for line in f:
            arr = line.split()
            u = arr[0]
            v = arr[1]
            t = arr[2]
            G.add_edge(int(u), int(v), weight=t)
    pos = nx.spring_layout(G)
    weights = nx.get_edge_attributes(G, "weight")
    nx.draw_networkx(G, pos, with_labels=True)
    nx.draw_networkx_edge_labels(G, pos, edge_labels=weights)
    plt.show()


if __name__ == '__main__':
    input_graph = input('Edgeliste eingeben: ')
    k = int(input('k eingeben: '))
    output_file = input_graph.split(".")[0] + '-DIJKSTRA-TOP-' + str(k) + '.txt'
    G = TemporalGraph([], [])
    G.import_edgelist(input_graph)
    G.node_ranking(0, np.inf, k, output_file)
    # /edge-lists/wiki_talk_nl            |  V = 225749 | E = 1554698
    # /edge-lists/wikipediasg.txt         |  V = 208142 | E = 810702
    # /edge-lists/facebook.txt            |  V = 63731  | E = 817036
    # /edge-lists/infectious.txt          |  V = 10972  | E = 415912
    # /edge-lists/tij_SFHH.txt            |  V = 3906   | E = 70261
    # /edge-lists/ht09_contact_list.txt   |  V = 5351   | E = 20817
    # /edge-lists/aves-weaver-social.txt  |  V = 445    | E = 1426
    # /edge-lists/test.txt                |  V = 7      | E = 18
    # /edge-lists/comparison.txt          |  V = 7      | E = 9