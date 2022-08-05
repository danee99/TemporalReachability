import multiprocessing
import os
import time
import heapq
import numpy as np

# path = os.path.join(os.getcwd(), os.pardir) + "\\edge-lists\\"
path = "/home/stud/degenste/BA/TemporalReachability/edge-lists/"


# def is_label_dominated(label, Q):
#     for item in Q:
#         if (label[1] < item[1] and label[0] >= item[0]) or (item[1] == label[1] and item[0] == label[0]):
#             return False
#     return True


class TemporalGraph:
    def __init__(self):
        self.nodes = set()
        self.incidence_list = []
        self.n = 0
        self.m = 0
        self.total_reachability = 0

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

    # def label_setting_fastest_path_algorithm(self, u):
    #     Q = []
    #     heapq.heappush(Q, (0, 0, u))
    #     d = [np.inf for _ in range(self.n)]
    #     d[u] = 0
    #     F = set()
    #     Pi = [np.inf for _ in range(self.n)]
    #     while Q:
    #         (a, s, v) = heapq.heappop(Q)
    #         if v in F:
    #             d[v] = a - s
    #             F.add(v)
    #         for (v, w, t, l) in self.incidence_list[v]:
    #             if a <= t:
    #                 if (a, s, v) == (0, 0, u):
    #                     label = (t + l, t, w)
    #                 else:
    #                     label = (t + l, s, w)
    #                 # Entferne die labels aus Pi[w] und Q, die dominiert werden 2 * O(n) ?
    #                 # (a0, s0, v) dominiert (a, s, v) wenn s < s0 und a >= a0, oder s = s0 und a > a0
    #                 # if label is not dominated: O(n) ?
    #                 if is_label_dominated(label, Q) == False:
    #                     heapq.heappush(Q, label)
    #                     Pi[w].add(label)
    #     return d

    # calculates the total reachability of the given temporal graph in a time interval [a,b]
    def calc_total_reachability(self, a, b):
        for node in self.nodes:
            reach_set = {node}
            visited = set()
            earliest_arrival_time = [np.inf for _ in range(self.n)]
            earliest_arrival_time[node] = a
            PQ = []
            heapq.heappush(PQ, (0, node))
            while PQ:
                (current_arrival_time, current_node) = heapq.heappop(PQ)
                visited.add(current_node)
                for (u, v, t, l) in self.incidence_list[current_node]:
                    if v not in visited:
                        if t < a or t + l > b: continue
                        if t + l < earliest_arrival_time[v] and t >= current_arrival_time:
                            # if earliest_arrival_time[v] != np.inf:
                            try:
                                PQ.remove((earliest_arrival_time[v], v))
                            except ValueError:
                                pass
                            reach_set.add(v)
                            earliest_arrival_time[v] = t + l
                            heapq.heappush(PQ, (earliest_arrival_time[v], v))
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
            earliest_arrival_time[node] = a
            PQ = []
            heapq.heappush(PQ, (0, node))
            while PQ:
                (current_arrival_time, current_node) = heapq.heappop(PQ)
                visited.add(current_node)
                for (u, v, t, l) in self.incidence_list[current_node]:
                    if u != x and v != x and v not in visited:
                        if t < a or t + l > b: continue
                        if t + l < earliest_arrival_time[v] and t >= current_arrival_time:
                            # if earliest_arrival_time[v] != np.inf:
                            try:
                                PQ.remove((earliest_arrival_time[v], v))
                            except ValueError:
                                pass
                            reach_set.add(v)
                            earliest_arrival_time[v] = t + l
                            heapq.heappush(PQ, (earliest_arrival_time[v], v))
            total += len(reach_set)
        return 1 - (total / before)
        # return total, x

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
            # ranking.sort()
            # for i in range(len(ranking)):
            #     f.write(str(i+1)+".Platz: "+str(ranking[i][1]) + "\n")
            f.write(str(ranking) + "\n")
            f.write("R(G) = %s" % self.total_reachability + "\n")
            f.write("abgeschlossen in %s Sekunden" % finish + "\n")
            f.write("abgeschlossen in %s Minuten" % (finish / 60) + "\n")
            f.write("abgeschlossen in %s Stunden" % (finish / 3600))


if __name__ == '__main__':
    input_graph = input('Edgeliste eingeben:')
    directed = (input('Soll die Kantenliste als gerichtet betrachtet werden? [y/n]:'))
    a = int(input('Intervall a eingeben: '))
    b = np.inf
    output_file = input_graph.split(".")[0] + '-PQ-Test' + '.txt'
    G = TemporalGraph()
    if directed == 'y':
        G.import_edgelist(input_graph)
    elif directed == 'n':
        G.import_undirected_edgelist(input_graph)
    G.node_ranking(a, b, output_file)