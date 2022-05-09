import os
import time
import heapq_max
import numpy as np


class TemporalGraph:
    def __init__(self, nodelist, edgelist):
        self.nodelist = []
        # self.out = []
        self.edgelist = []

    # outputs the set of nodes and each temporal edge as well as the outdegreee array
    def print_graph(self):
        for i in self.edgelist:
            print(*i)
        print(self.nodelist)
        # print(self.out)

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
                    # self.out.append(0)
                if v not in self.nodelist:
                    self.nodelist.append(v)
                    # self.out.append(0)
                # self.out[u] = self.out[u] + 1
                self.edgelist.append((u, v, t, l))
        # self.nodelist = [x for _, x in sorted(zip(self.out, self.nodelist), reverse=True)]

    # calculates how many nodes can be reached from a node in O(n+m) for an interval [a,b]
    def calc_reachable_nodes(self, node, a, b):
        reach_num = 1
        min_at = [np.inf for i in range(0, len(self.nodelist))]
        min_at[node] = 0
        for (u, v, t, l) in self.edgelist:
            if t < a or t + l > b: continue
            if min_at[u] <= t:
                if min_at[v] > t + 1:
                    min_at[v] = t + 1
                    reach_num = reach_num + 1
        return reach_num

    # calculates the total reachability (sum of the vector) of the entire graph in O(n^2 + nm)
    def total_reachability(self, a, b):
        result = []
        for node in self.nodelist:
            result.append(self.calc_reachable_nodes(node, a, b))
        return sum(result)

    # calculates the total reachability of the entire graph after deleting "node"
    # this is the helper function for the top k nodes
    def total_reachability_after(self, a, b, node, my_heap, k, h):
        result = 0
        count = 0
        for x in self.nodelist:
            count = count + 1
            reach_num = 1
            if x == node:
                reach_num = 0
            min_at = h.copy()
            min_at[x] = 0
            for (u, v, t, l) in self.edgelist:
                if u != node and v != node:
                    if t < a or t + l > b: continue
                    if min_at[u] <= t:
                        if min_at[v] > t + 1:
                            min_at[v] = t + 1
                            reach_num = reach_num + 1
            result = result + reach_num
            if my_heap != [] and len(my_heap) >= k:
                if result > my_heap[0][0]:
                    return -1
        return result

    # outputs the top k nodes
    def top_k_nodes(self, a, b, k, output_name):
        max_heap = []
        start_time = time.time()
        h = [np.inf for i in range(0, len(self.nodelist))]
        for node in self.nodelist:
            R = self.total_reachability_after(a, b, node, max_heap, k, h)
            if R == -1:
                continue
            if len(max_heap) < k:
                heapq_max.heappush_max(max_heap, (R, node))
            else:
                if R < max_heap[0][0]:
                    heapq_max.heappushpop_max(max_heap, (R, node))
        with open(os.getcwd() + output_name, 'w') as f:
            f.write(str(max_heap)+"\n")
            f.write("--- finished in %s seconds ---" % (time.time() - start_time))


if __name__ == '__main__':
    data = input('Edgeliste eingeben: ')
    k = int(input('k eingeben: '))
    output = data.split(".")[0] + '-FAST-TOP-' + str(k) + '.txt'
    G = TemporalGraph([], [])
    G.import_edgelist(data)
    G.top_k_nodes(0, np.inf, k, output)
    # /edge-lists/wikipediasg.txt         |  V = 208142 | E = 810702
    # /edge-lists/facebook.txt            |  V = 63731  | E = 817036
    # /edge-lists/infectious.txt          |  V = 10972  | E = 415912
    # /edge-lists/tij_SFHH.txt            |  V = 3906   | E = 70261
    # /edge-lists/ht09_contact_list.txt   |  V = 5351   | E = 20817
    # /edge-lists/aves-weaver-social.txt  |  V = 445    | E = 1426
    # /edge-lists/test.txt                |  V = 7      | E = 18
    # /edge-lists/comparison.txt          |  V = 7      | E = 9
