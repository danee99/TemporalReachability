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
            # earliest_arrival_time = [np.inf for _ in range(len(self.nodes))]
            earliest_arrival_time = {v: np.inf for v in self.nodes}
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

    def rank_node(self, x, a, b, before, helper):
        total = 0
        for node in self.nodes:
            if node == x:
                continue
            reach_set = {node}
            visited = set()
            earliest_arrival_time = helper[:]
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
        helper = [np.inf for _ in range(self.n)]
        self.calc_total_reachability(a, b)
        start_time2 = time.time()
        pool = multiprocessing.Pool(multiprocessing.cpu_count())
        result_objects = [pool.apply_async(self.rank_node, args=(node, a, b, self.total_reachability, helper)) for node
                          in range(0, self.n)]
        ranking = [r.get() for r in result_objects]
        finish2 = time.time() - start_time2
        pool.close()
        pool.join()
        finish = time.time() - start_time
        with open(os.getcwd() + output_name, 'w') as f:
            f.write(str(ranking) + "\n")
            f.write("R(G) = " + str(self.total_reachability) + "\n")
            f.write("--- ranking finished in %s seconds ---" % finish + "\n")
            f.write("--- finished in %s seconds ---" % finish + "\n")
            f.write("--- finished in %s minutes ---" % (finish / 60) + "\n")
            f.write("--- finished in %s hours ---" % (finish / 3600))

    def calculate_bounds(self, a, b, x, helper):
        upper_bound = 0
        lower_bound = 0
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
                    for (u, v, t, l) in self.graph[current_node]:
                        if u != x and v != x:
                            if t < a or t + l > b: continue
                            if t + l < earliest_arrival_time[v] and t >= current_arrival_time:
                                reach_set.add(v)
                                earliest_arrival_time[v] = t + l
                                PQ.put((earliest_arrival_time[v], v))
                    visited.add(current_node)
            # first, we calculate all reachabilities normally
            lower_bound += len(reach_set)
            # for the upper bound, we have to assume that the node for which the reachabilities are currently being
            # calculated could theoretically reach any deleted node in the original graph
            upper_bound += len(reach_set) + len(self.deleted_nodes)
        # finally, we need to add the part that definitely falls away for the "correct" total reachability
        lower_bound += sum(len(value) for key, value in self.change_in_reachability.items()
                           if key != x)
        upper_bound += sum(len(value) for key, value in self.change_in_reachability.items()
                           if key in self.deleted_nodes)
        return x, (lower_bound, upper_bound)

    def filter_nodes(self, depth):
        for i in range(0, depth):
            # find all nodes that have a degree of 0 in the current graph
            for node in self.nodes:
                # if outdegree = 0 --> add node to the set of nodes that will be deleted from the graph
                if self.nodes[node][0] == 0:
                    self.deleted_nodes.add(node)
                    # the fact that the node could reach itself would be omitted
                    # so we have to remember that the node could reach itself
                    if node not in self.change_in_reachability:
                        self.change_in_reachability[node] = set()
                    self.change_in_reachability[node].add(node)
            for node in self.nodes:
                for (u, v, t, l) in self.graph[node][:]:
                    if v in self.deleted_nodes:
                        if u not in self.change_in_reachability:
                            self.change_in_reachability[u] = set()
                        # this is the part that would be skipped when calculating r(u)
                        self.change_in_reachability[u].add(v)
                        # outdegree of u is reduced
                        self.nodes[u][0] -= 1
                        # indegree of v is reduced
                        self.nodes[v][1] -= 1
                        # delete edge from the graph and decrease number of edges by 1
                        self.graph[u].remove((u, v, t, l))
                        self.m -= 1
            # delete all nodes that were detected and decrease number of nodes
            for node in self.deleted_nodes:
                try:
                    del self.nodes[node]
                    del self.graph[node]
                    self.n -= 1
                except KeyError:
                    continue

    def heuristik(self, a, b, output_name, depth):
        start_time1 = time.time()
        self.filter_nodes(depth)
        finish_filternodes = time.time() - start_time1

        start_time2 = time.time()
        helper = {v: np.inf for v in self.nodes}
        finish_helper = time.time() - start_time2

        start_time3 = time.time()
        pool = multiprocessing.Pool(multiprocessing.cpu_count())
        result_objects = [pool.apply_async(self.calculate_bounds, args=(a, b, node, helper)) for node in self.nodes]
        ranking = [r.get() for r in result_objects]
        finish_rank = time.time() - start_time3

        pool.close()
        pool.join()
        finish_total = time.time() - start_time1
        with open(os.getcwd() + output_name, 'w') as f:
            ranking.sort(key=lambda tup: tup[1][0])
            f.write(str(ranking) + "\n")
            f.write("mit Tiefe = " + str(depth) + "\n")
            f.write("geloeschte Knotenanzahl = " + str(len(self.deleted_nodes)) + "\n")
            f.write("uebrige Kanten = " + str(self.m) + "\n")
            f.write("--- filter_nodes() finished in %s seconds ---" % finish_filternodes + "\n")
            f.write("--- creating the helper finished in %s seconds ---" % finish_helper + "\n")
            f.write("--- ranking finished in %s seconds ---" % finish_rank + "\n")
            f.write("--- total finished in %s seconds ---" % finish_total + "\n")
            # f.write("--- finished in %s seconds ---" % finish_total + "\n")
            # f.write("--- filter_nodes() finished in %s minutes ---" % (finish1 / 60) + "\n")
            # f.write("--- finished in %s minutes ---" % (finish2 / 60) + "\n")
            # f.write("--- finished in %s hours ---" % (finish2 / 3600))


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
