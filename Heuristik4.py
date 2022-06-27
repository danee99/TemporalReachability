import multiprocessing
import os
import time
from queue import PriorityQueue
import numpy as np


class TemporalGraph:
    def __init__(self):
        self.n = 0
        self.m = 0
        self.nodes = {}
        self.graph = {}
        self.deleted_nodes = set()
        self.total_reachability = 0
        self.change_in_reachability = {}
        # outdegree(v) = self.nodes[v][0]
        # indegree(v) = self.nodes[v][1]

    def add_edge(self, u, v, t, l):
        if u in self.graph:
            self.graph[u].append((u, v, t, l))
        else:
            self.graph[u] = [(u, v, t, l)]
        if u in self.nodes:
            self.nodes[u][0] += 1
        else:
            self.nodes[u] = [1, 0]
        if v not in self.graph:
            self.graph[v] = []
        if v in self.nodes:
            self.nodes[v][1] += 1
        else:
            self.nodes[v] = [0, 1]
        self.m += 1

    def print_graph(self):
        print("|V| = " + str(self.n))
        print("|E| = " + str(self.m))
        for v in self.graph:
            print(str(v) + " " + str(self.graph[v]))
            # print(str(v) + " " + str(self.nodes[v]))

    def import_edgelist(self, file_name):
        with open(os.getcwd() + file_name, "r") as f:
            self.n = int(f.readline())
            for line in f:
                arr = line.split()
                u = int(arr[0])
                v = int(arr[1])
                t = int(arr[2])
                l = int(arr[3])
                self.add_edge(u, v, t, l)

    def calc_total_reachability(self, a, b):
        for node in self.nodes:
            reach_set = {node}
            earliest_arrival_time = [np.inf for _ in range(len(self.nodes))]
            earliest_arrival_time[node] = 0
            PQ = PriorityQueue()
            PQ.put((earliest_arrival_time[node], node))
            while not PQ.empty():
                (current_arrival_time, current_node) = PQ.get()
                for (u, v, t, l) in self.graph[current_node]:
                    if t < a or t + l > b: continue
                    if t + l < earliest_arrival_time[v] and t >= current_arrival_time:
                        reach_set.add(v)
                        earliest_arrival_time[v] = t + l
                        PQ.put((earliest_arrival_time[v], v))
            self.total_reachability += len(reach_set)

    def rank_node(self, x, a, b, before):
        total = 0
        for node in self.nodes:
            if node == x:
                continue
            reach_set = {node}
            visited = set()
            earliest_arrival_time = [np.inf for _ in range(self.n)]
            earliest_arrival_time[node] = 0
            PQ = PriorityQueue()
            PQ.put((earliest_arrival_time[node], node))
            while not PQ.empty():
                (current_arrival_time, current_node) = PQ.get()
                if current_node not in visited:
                    for (u, v, t, l) in self.graph[current_node]:
                        if u != x and v != x:
                            if t < a or t + l > b: continue
                            if t + l < earliest_arrival_time[v] and t >= current_arrival_time:
                                reach_set.add(v)
                                earliest_arrival_time[v] = t + l
                                PQ.put((earliest_arrival_time[v], v))
                    visited.add(current_node)
            total += len(reach_set)
        return 1 - (total / before)

    def node_ranking(self, a, b, output_name):
        start_time = time.time()
        self.calc_total_reachability(a, b)
        pool = multiprocessing.Pool(multiprocessing.cpu_count())
        result_objects = [pool.apply_async(self.rank_node, args=(node, a, b, self.total_reachability)) for node in
                          range(0, self.n)]
        ranking = [r.get() for r in result_objects]
        pool.close()
        pool.join()
        finish = time.time() - start_time
        with open(os.getcwd() + output_name, 'w') as f:
            f.write(str(ranking) + "\n")
            f.write("--- finished in %s seconds ---" % finish + "\n")
            f.write("--- finished in %s minutes ---" % (finish / 60) + "\n")
            f.write("--- finished in %s hours ---" % (finish / 3600))

    def calculate_bounds(self, a, b, x):
        upper_bound = 0
        lower_bound = 0
        for node in self.nodes:
            if node == x:
                continue
            reach_set = {node}
            visited = set()
            earliest_arrival_time = {v: np.inf for v in self.nodes}
            earliest_arrival_time[node] = 0
            PQ = PriorityQueue()
            PQ.put((earliest_arrival_time[node], node))
            while not PQ.empty():
                (current_arrival_time, current_node) = PQ.get()
                if current_node not in visited:
                    for (u, v, t, l) in self.graph[current_node]:
                        if u != x and v != x:
                            if t < a or t + l > b: continue
                            if t + l < earliest_arrival_time[v] and t >= current_arrival_time:
                                reach_set.add(v)
                                earliest_arrival_time[v] = t + l
                                PQ.put((earliest_arrival_time[v], v))
                    visited.add(current_node)
            lower_bound += len(reach_set)
            upper_bound += len(reach_set) + len(self.deleted_nodes)
        lower_bound += sum(len(value) for key, value in self.change_in_reachability.items()
                           if key != x)
        upper_bound += sum(len(value) for key, value in self.change_in_reachability.items()
                           if key in self.deleted_nodes)
        return x, (lower_bound, upper_bound)

    def filter_nodes(self, depth):
        for i in range(0, depth):
            for node in self.nodes:
                if self.nodes[node][0] == 0:
                    self.deleted_nodes.add(node)
                    if node not in self.change_in_reachability:
                        self.change_in_reachability[node] = set()
                    self.change_in_reachability[node].add(node)
            for node in self.nodes:
                for (u, v, t, l) in self.graph[node][:]:
                    if v in self.deleted_nodes:
                        if u not in self.change_in_reachability:
                            self.change_in_reachability[u] = set()
                        self.change_in_reachability[u].add(v)
                        self.nodes[u][0] -= 1
                        self.nodes[v][1] -= 1
                        self.graph[u].remove((u, v, t, l))
                        self.m -= 1
            for node in self.deleted_nodes:
                try:
                    del self.nodes[node]
                    del self.graph[node]
                    self.n -= 1
                except KeyError:
                    continue

    # def filter_nodes2(self, depth):
    #     i = 0
    #     while i != depth:
    #         for node in self.nodes:
    #             if self.nodes[node][1] == 0:
    #                 self.deleted_nodes.add(node)
    #         for node in self.nodes:
    #             for (u, v, t, l) in self.graph[node][:]:
    #                 if v in self.deleted_nodes:
    #                     self.change_in_reachability[u] += 1
    #                     self.nodes[u][1] -= 1
    #                     self.nodes[v][2] -= 1
    #                     self.graph[u].remove((u, v, t, l))
    #                     self.m -= 1
    #         for node in self.deleted_nodes:
    #             try:
    #                 del self.nodes[node]
    #                 del self.graph[node]
    #                 self.n -= 1
    #             except KeyError:
    #                 continue
    #         i += 1

    def heuristik(self, a, b, output_name, depth):
        start_time = time.time()
        self.filter_nodes(depth)
        finish1 = time.time() - start_time
        pool = multiprocessing.Pool(multiprocessing.cpu_count())
        result_objects = [pool.apply_async(self.calculate_bounds, args=(a, b, node)) for node in self.nodes]
        ranking = [r.get() for r in result_objects]
        pool.close()
        pool.join()
        finish2 = time.time() - start_time
        with open(os.getcwd() + output_name, 'w') as f:
            ranking.sort(key=lambda tup: tup[1][0])
            f.write(str(ranking) + "\n")
            f.write("mit Tiefe = " + str(depth) + "\n")
            f.write("--- finished in %s seconds ---" % finish2 + "\n")
            f.write("--- filter_nodes() finished in %s minutes ---" % (finish1 / 60) + "\n")
            f.write("--- finished in %s minutes ---" % (finish2 / 60) + "\n")
            f.write("--- finished in %s hours ---" % (finish2 / 3600))


if __name__ == '__main__':
    input_graph = '/edge-lists/' + input('Edgeliste eingeben:')
    depth = int(input('Tiefe eingeben:'))
    heuristik_output_file = input_graph.split(".")[0] + '-Heuristik' + '.txt'
    ranking_output_file = input_graph.split(".")[0] + '-Rangliste' + '.txt'
    # test = input_graph.split(".")[0] + '-_TEST' + '.txt'
    G = TemporalGraph()
    G.import_edgelist(input_graph)
    G.node_ranking(0, np.inf, ranking_output_file)
    G.heuristik(0, np.inf, heuristik_output_file, depth)
    # Rangliste 13.939621333281199 min
    # Heuristik  5.106800317764282 min
