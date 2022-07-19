import multiprocessing
import os
import time
import numpy as np

# path = os.path.join(os.getcwd(), os.pardir) + "\\edge-lists\\"
path = "/home/stud/degenste/BA/TemporalReachability/edge-lists/"

class TemporalGraph:
    def __init__(self):
        self.nodes = []
        self.edge_stream = []
        self.n = 0

    def import_edgelist(self, file_name):
        with open(path + file_name, "r") as f:
            n = int(f.readline())
            self.n = n
            self.nodes = [i for i in range(0, n)]
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
            self.nodes = [i for i in range(0, n)]
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
            total_reach = total_reach + reach_num
        return total_reach

    def rank_node(self, a, b, x, helper, before):
        total_reach = 0
        for node in self.nodes:
            if node == x:
                continue
            reach_num = 1
            arrival_time = helper.copy()
            arrival_time[node] = a
            for (u, v, t, l) in self.edge_stream:
                if u != x and v != x:
                    if t < a or t + l > b: continue
                    if arrival_time[u] <= t and arrival_time[v] > t + l:
                        arrival_time[v] = t + l
                        reach_num = reach_num + 1
            total_reach = total_reach + reach_num
        return 1 - (total_reach / before), x
        # return total_reach

    def node_ranking(self, a, b, output_name):
        start_time = time.time()
        before = self.total_reachability(a, b)
        helper = [np.inf for _ in range(self.n)]
        pool = multiprocessing.Pool(multiprocessing.cpu_count())
        result_objects = [pool.apply_async(self.rank_node, args=(a, b, node, helper, before)) for node in
                          range(0, self.n)]
        ranking = [r.get() for r in result_objects]
        pool.close()
        pool.join()
        finish = time.time() - start_time
        with open(path + output_name, 'w') as f:
            ranking.sort(key=lambda tup: tup[0], reverse=True)
            f.write(str(ranking) + "\n")
            f.write("abgeschlossen in %s Sekunden" % finish + "\n")
            f.write("abgeschlossen in %s Minuten" % (finish / 60) + "\n")
            f.write("abgeschlossen in %s Stunden" % (finish / 3600))


if __name__ == '__main__':
    input_graph = input('Edgeliste eingeben:')
    directed = (input('Ist der Graph gerichtet? [y/n]:'))
    output_file = input_graph.split(".")[0] + '-Streaming-Ranking' + '.txt'
    G = TemporalGraph()
    if directed == 'y':
        G.import_edgelist(input_graph)
    elif directed == 'n':
        G.import_undirected_edgelist(input_graph)
    G.node_ranking(0, np.inf, output_file)
