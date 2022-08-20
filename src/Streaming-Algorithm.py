import multiprocessing
import os
import time
import numpy as np
from queue import PriorityQueue
import heapq_max

# path = os.path.join(os.getcwd(), os.pardir) + "\\edge-lists\\"
path = "/home/stud/degenste/BA/TemporalReachability/edge-lists/"
max_heap = []
k = 10


def log_result(result):
    if result[0] != -1:
        if len(max_heap) < k:
            heapq_max.heappush_max(max_heap, (result[0], result[1]))
        if len(max_heap) >= k:
            if result[0] < max_heap[0][0]:
                heapq_max.heappushpop_max(max_heap, (result[0], result[1]))


class TemporalGraph:
    def __init__(self):
        self.nodes = []
        self.edge_stream = []
        self.n = 0

    def import_edgelist(self, file_name):
        with open(path + file_name, "r") as f:
            n = int(f.readline())
            self.n = n
            self.nodes = [i for i in range(n)]
            for line in f:
                arr = line.split()
                u = int(arr[0])
                v = int(arr[1])
                t = int(arr[2])
                try:
                    l = int(arr[3])
                except IndexError:
                    l = 1
                self.edge_stream.append((u, v, t, l))

    def import_undirected_edgelist(self, file_name):
        with open(path + file_name, "r") as f:
            n = int(f.readline())
            self.n = n
            self.nodes = [i for i in range(n)]
            for line in f:
                arr = line.split()
                u = int(arr[0])
                v = int(arr[1])
                t = int(arr[2])
                try:
                    l = int(arr[3])
                except IndexError:
                    l = 1
                self.edge_stream.append((u, v, t, l))
                self.edge_stream.append((v, u, t, l))

    def total_reachability(self, a, b):
        total_reach = 0
        for node in self.nodes:
            reach_num = 1
            arrival_time = [np.inf for _ in range(self.n)]
            arrival_time[node] = a
            for (u, v, t, l) in self.edge_stream:
                if t >= a and b >= l:
                    if arrival_time[u] <= t and arrival_time[v] > t + l:
                        arrival_time[v] = t + l
                        reach_num = reach_num + 1
            total_reach += reach_num
        return total_reach

    def rank_node(self, a, b, x, before, helper):
        total_reach = 0
        for node in self.nodes:
            if node == x:
                continue
            reach_num = 1
            arrival_time = helper.copy()
            arrival_time[node] = a
            for (u, v, t, l) in self.edge_stream:
                if u != x and v != x:
                    if t < a or t + l > b: break
                    if arrival_time[u] <= t and arrival_time[v] > t + l:
                        arrival_time[v] = t + l
                        reach_num = reach_num + 1
            total_reach += reach_num
        return 1 - (total_reach / before), x
        # return 1 - (total_reach / before)
        # return total_reach

    def node_ranking(self, a, b, output_name):
        # start_time = time.time()
        # before = self.total_reachability(a, b)
        # helper = [np.inf for _ in range(self.n)]
        # pool = multiprocessing.Pool(multiprocessing.cpu_count())
        # result_objects = [pool.apply_async(self.rank_node, args=(a, b, node, helper, before)) for node in
        #                   range(0, self.n)]
        # ranking = [r.get() for r in result_objects]
        # pool.close()
        # pool.join()
        # finish = time.time() - start_time
        # with open(path + output_name, 'w') as f:
        #     # ranking.sort(key=lambda tup: tup[0], reverse=True)
        #     # ranking.sort(reverse=True)
        #     # f.write(str([v for (rank, v) in ranking[:k]]) + "\n")
        #     f.write(str(ranking) + "\n")
        #     f.write("R(G) = %s" % before + "\n")
        #     f.write("abgeschlossen in %s Sekunden" % finish + "\n")
        #     f.write("abgeschlossen in %s Minuten" % (finish / 60) + "\n")
        #     f.write("abgeschlossen in %s Stunden" % (finish / 3600))
        start_time = time.time()
        before = self.total_reachability(a, b)
        helper = [np.inf for _ in range(self.n)]
        ranking = []
        for node in range(0, self.n):
            ranking.append(self.rank_node(a, b, node, before, helper))
        finish = time.time() - start_time
        with open(path + output_name, 'w') as f:
            # f.write(str(ranking) + "\n")
            ranking.sort(reverse=True)
            for i in range(len(ranking)):
                f.write(str(i + 1) + ".Platz: " + str(ranking[i][1]) + "\n")
            f.write("R(G) = %s" % before + "\n")
            f.write("abgeschlossen in %s Sekunden" % finish + "\n")
            f.write("abgeschlossen in %s Minuten" % (finish / 60) + "\n")
            f.write("abgeschlossen in %s Stunden" % (finish / 3600))

    def top_k_util(self, x, a, b, helper):
        total = 0
        for node in self.nodes:
            if node == x:
                continue
            reach_num = 1
            arrival_time = helper.copy()
            arrival_time[node] = a
            for (u, v, t, l) in self.edge_stream:
                if u != x and v != x:
                    if t < a or t + l > b: break
                    if arrival_time[u] <= t and arrival_time[v] > t + l:
                        arrival_time[v] = t + l
                        reach_num = reach_num + 1
            total += reach_num
            if max_heap != [] and len(max_heap) >= k and total > max_heap[0][0]:
                return -1, x
        return total, x

    def top_k_reachability(self, alpha, beta, k, output_name):
        start_time = time.time()
        helper = [np.inf for _ in range(self.n)]
        pool = multiprocessing.Pool(multiprocessing.cpu_count())
        for node in self.nodes:
            pool.apply_async(self.top_k_util, args=(node, alpha, beta, helper), callback=log_result)
        pool.close()
        pool.join()
        finish = time.time() - start_time
        with open(path + output_name, 'w') as f:
            max_heap.sort()
            f.write(str(max_heap) + "\n")
            f.write("abgeschlossen in %s Sekunden" % finish + "\n")
            f.write("abgeschlossen in %s Minuten" % (finish / 60) + "\n")
            f.write("abgeschlossen in %s Stunden" % (finish / 3600))


if __name__ == '__main__':
    input_graph = input('Edgeliste eingeben:')
    directed = (input('Soll die Kantenliste als gerichtet betrachtet werden? [y/n]:'))
    run_topk = (input('Soll der Top-K-Algorithmus durchgeführt werden? [y/n]:'))
    output_file = input_graph.split(".")[0] + '-Streaming-Ranking' + '.txt'
    topk_file = input_graph.split(".")[0] + '-Top' + str(k) + '.txt'
    G = TemporalGraph()
    if directed == 'y':
        G.import_edgelist(input_graph)
    elif directed == 'n':
        G.import_undirected_edgelist(input_graph)
    if run_topk == 'y':
        G.top_k_reachability(0, np.inf, k, topk_file)
    elif run_topk == 'n':
        G.node_ranking(0, np.inf, output_file)