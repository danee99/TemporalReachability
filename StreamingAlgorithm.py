import multiprocessing
import os
import time
from queue import PriorityQueue
import numpy as np


class TemporalGraph:
    def __init__(self):
        self.nodes = []
        self.edge_stream = []
        self.n = 0

    # scans an edgelist and creates a TemporalGraph object in O(n+m)
    def import_edgelist(self, file_name):
        with open(os.getcwd() + file_name, "r") as f:
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

    def total_reachability(self, a, b):
        total_reach = 0
        for node in self.nodes:
            reach_num = 1
            arrival_time = [np.inf for _ in range(self.n)]
            arrival_time[node] = 0
            for (u, v, t, l) in self.edge_stream:
                if t >= a and l <= b:
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
            arrival_time[node] = 0
            for (u, v, t, l) in self.edge_stream:
                if u != x and v != x:
                    if t < a or t + l > b: continue
                    if arrival_time[u] <= t and arrival_time[v] > t + l:
                        arrival_time[v] = t + l
                        reach_num = reach_num + 1
            total_reach = total_reach + reach_num
        return 1 - total_reach/before

    # node ranking, but with asynchronous multiprocessing
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
        with open(os.getcwd() + output_name, 'w') as f:
            f.write(str(ranking) + "\n")
            finish = time.time() - start_time
            f.write("--- finished in %s seconds ---" % finish + "\n")
            f.write("--- finished in %s minutes ---" % (finish / 60) + "\n")
            f.write("--- finished in %s hours ---" % (finish / 3600))


if __name__ == '__main__':
    input_graph = '/edge-lists/' + input('Edgeliste eingeben:')
    a = int(input('Intervall a eingeben: '))
    b = np.inf
    output_file = input_graph.split(".")[0] + '-Streaming-Rangliste' + '.txt'
    G = TemporalGraph()
    G.import_edgelist(input_graph)
    G.node_ranking(a, b, output_file)
    # DATASETS:
    # /edge-lists/wiki_talk_nl.txt          |  |V| = 225.749 | |E| = 1.554.698
    # /edge-lists/wikipediasg.txt           |  |V| = 208.142 | |E| = 810.702
    # /edge-lists/facebook.txt              |  |V| = 63.731  | |E| = 817.035
    # /edge-lists/twitter.txt               |  |V| = 4.605   | |E| = 23.736     352.0 min vs 393.8 min
    # /edge-lists/ia-reality-call.txt       |  |V| = 6.809   | |E| = 52.050     307.1 min
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
