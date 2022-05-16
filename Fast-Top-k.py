import heapq
import multiprocessing
import os
import time
import numpy as np

result_list = []


def log_result(result):
    heapq.heappush(result_list, result)


class TemporalGraph:
    def __init__(self, nodelist, edgelist):
        self.nodelist = []
        # self.out = []
        self.edgelist = []

    # Assumption: edge stream representation, i.e. edges are sorted by timestamps
    # scans the edgelist and adds all nodes and edges to the graph
    def import_edgelist(self, file_name):
        with open(os.getcwd() + file_name, "r") as f:
            n = int(f.readline())
            for line in f:
                arr = line.split()
                u = int(arr[0])
                v = int(arr[1])
                t = int(arr[2])
                try:
                    l = int(arr[3])
                except IndexError:
                    l = 1
                if u not in self.nodelist:
                    self.nodelist.append(u)
                    # self.out.append(0)
                if v not in self.nodelist:
                    self.nodelist.append(v)
                    # self.out.append(0)
                # self.out[u] = self.out[u] + 1
                self.edgelist.append((u, v, t, l))
        # self.nodelist = [x for _, x in sorted(zip(self.out, self.nodelist), reverse=True)]

    def total_reachability_after(self, a, b, node, help_list):
        total_reach = 0
        for x in self.nodelist:
            reach_num = 1
            if x == node:
                reach_num = 0
            min_at = help_list.copy()
            min_at[x] = 0
            for (u, v, t, l) in self.edgelist:
                if u != node and v != node:
                    if t < a or t + l > b: continue
                    if min_at[u] <= t:
                        if min_at[v] > t + 1:
                            min_at[v] = t + 1
                            reach_num = reach_num + 1
            total_reach = total_reach + reach_num
        return total_reach, node

    def top_k_nodes(self, a, b, k, output_name):
        start_time = time.time()
        help_list = [np.inf for i in range(0, len(self.nodelist))]
        pool = multiprocessing.Pool(multiprocessing.cpu_count())
        for node in self.nodelist:
            pool.apply_async(self.total_reachability_after, args=(a, b, node, help_list), callback=log_result)
        pool.close()
        pool.join()
        with open(os.getcwd() + output_name, 'w') as f:
            f.write(str(heapq.nsmallest(k, result_list)) + "\n")
            finish = time.time() - start_time
            f.write("--- finished in %s seconds ---" % (finish) + "\n")
            f.write("--- finished in %s minutes ---" % ((finish) / 60) + "\n")
            f.write("--- finished in %s hours ---" % ((finish) / 3600))


if __name__ == '__main__':
    data = input('Edgeliste eingeben: ')
    k = int(input('k eingeben: '))
    output = data.split(".")[0] + '-FAST-TOP-' + str(k) + '.txt'
    G = TemporalGraph([], [])
    G.import_edgelist(data)
    G.top_k_nodes(0, np.inf, k, output)
    # /edge-lists/wiki_talk_nl            |  V = 225749 | E = 1554698
    # /edge-lists/wikipediasg.txt         |  V = 208142 | E = 810702
    # /edge-lists/facebook.txt            |  V = 63731  | E = 817036
    # /edge-lists/infectious.txt          |  V = 10972  | E = 415912
    # /edge-lists/tij_SFHH.txt            |  V = 3906   | E = 70261
    # /edge-lists/ht09_contact_list.txt   |  V = 5351   | E = 20817
    # /edge-lists/aves-weaver-social.txt  |  V = 445    | E = 1426
    # /edge-lists/test.txt                |  V = 7      | E = 18
    # /edge-lists/comparison.txt          |  V = 7      | E = 9