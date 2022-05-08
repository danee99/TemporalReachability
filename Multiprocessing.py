import os
import time
import numpy as np
import heapq_max
import threading
import multiprocessing

result_list = []
def log_result(result):
    result_list.append(result)

class TemporalGraph:
    def __init__(self, nodelist, edgelist):
        self.nodelist = []
        self.out = []
        self.edgelist = []

    # Assumption: edge stream representation, i.e. edges are sorted by timestamps
    # scans the edgelist and adds all nodes and edges to the graph
    def import_edgelist(self, file_name):
        with open(os.getcwd() + file_name, "r") as f:
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
                    self.out.append(0)
                if v not in self.nodelist:
                    self.nodelist.append(v)
                    self.out.append(0)
                self.out[u] = self.out[u] + 1
                self.edgelist.append((u, v, t, l))
        self.nodelist = [x for _, x in sorted(zip(self.out, self.nodelist), reverse=True)]

    # calculates the total reachability of the entire graph after deleting "node"
    # this is the helper function for the top k nodes
    def total_reachability_after(self, a, b, node, max_heap, k, help_list):
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
            if max_heap != [] and len(max_heap) >= k:
                if total_reach > max_heap[0][0]:
                    # return -1
                    break
        if len(max_heap) < k:
            heapq_max.heappush_max(max_heap, (total_reach, node))
        else:
            if total_reach < max_heap[0][0]:
                heapq_max.heappushpop_max(max_heap, (total_reach, node))
        # return total_reach

    # outputs the top k nodes
    def top_k_nodes(self, a, b, k):
        start_time = time.time()
        max_heap = []
        help_list = [np.inf for i in range(0, len(self.nodelist))]
        threads = []
        for node in self.nodelist:
            t = threading.Thread(target=self.total_reachability_after, args=(a, b, node, max_heap, k, help_list,))
            t.start()
            threads.append(t)
            for thread in threads:
                thread.join()
            continue
        print(str(max_heap) + "\n")
        print("--- finished in %s seconds ---" % (time.time() - start_time))

    def inner(self, a, b, node, help_list):
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
        return total_reach

    def outer(self, a, b, k):
        start_time = time.time()
        help_list = [np.inf for i in range(0, len(self.nodelist))]
        results = []
        pool = multiprocessing.Pool(multiprocessing.cpu_count())
        for node in self.nodelist:
            # results.append(self.inner(a, b, node, help_list))
            # results.append(pool.apply_async(self.inner, args=(a, b, node, help_list)))
            # self.get_result(results, self.inner(a, b, node, help_list))
            pool.apply_async(self.inner, args=(a, b, node, help_list), callback = log_result)
        pool.close()
        pool.join()
        # results.sort()
        print(result_list)
        print(results)
        print("--- finished in %s seconds ---" % (time.time() - start_time))


if __name__ == '__main__':
    data = '\\edge-lists\\aves-weaver-social.txt'
    output1 = '\\edge-lists\\hallo.txt'
    output = data.split(".")[0] + '-Ranking' + '.txt'
    G = TemporalGraph([], [])
    G.import_edgelist(data)
    G.outer(0, np.inf, 3)
    # /edge-lists/wikipediasg.txt         |  V = 208142 | E = 810702
    # /edge-lists/facebook.txt            |  V = 63731  | E = 817036
    # /edge-lists/infectious.txt          |  V = 10972  | E = 415912
    # /edge-lists/tij_SFHH.txt            |  V = 3906   | E = 70261
    # /edge-lists/ht09_contact_list.txt   |  V = 5351   | E = 20817
    # /edge-lists/aves-weaver-social.txt  |  V = 445    | E = 1426
    # /edge-lists/test.txt                |  V = 7      | E = 18
    # \\edge-lists\\aves-weaver-social.txt  --> \\edge-lists\\hallo.txt
