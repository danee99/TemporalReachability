import heapq
import math
import time
from io import StringIO

import numpy as np


def show_tree(tree, total_width=60, fill=' '):
    """Pretty-print a tree.
    total_width depends on your input size"""
    output = StringIO()
    last_row = -1
    for i, n in enumerate(tree):
        if i:
            row = int(math.floor(math.log(i + 1, 2)))
        else:
            row = 0
        if row != last_row:
            output.write('\n')
        columns = 2 ** row
        col_width = int(math.floor((total_width * 1.0) / columns))
        output.write(str(n).center(col_width, fill))
        last_row = row
    print(output.getvalue())
    print('-' * total_width)
    return


class TemporalGraph:
    def __init__(self, nodemanager, edgelist):
        self.nodemanager = {}
        # keys = node ids --> values = [0 ... n-1]
        self.nodelist = self.nodemanager.values()
        self.edgelist = []

    # outputs the set of nodes and the set of edges
    def print_graph(self):
        for i in self.edgelist:
            print(*i)
        print(self.nodemanager)
        print(self.nodelist)

    # Assumption: Input graph is in edge stream representation, i.e. edges are sorted by timestamps
    def import_edgelist(self, file_name):
        file = 'edge-lists\\' + file_name
        with open(file) as fp:
            val = 0
            for line in fp:
                arr = line.split()
                u = int(arr[0])
                v = int(arr[1])
                t = int(arr[2])
                try:
                    l = int(arr[3])
                except IndexError:
                    l = 1
                if u not in self.nodemanager.keys():
                    self.nodemanager.update({u: val})
                    val = val + 1
                if v not in self.nodemanager.keys():
                    self.nodemanager.update({v: val})
                    val = val + 1
                if (self.nodemanager[u], self.nodemanager[v], t, l) not in self.edgelist:
                    self.edgelist.append((self.nodemanager[u], self.nodemanager[v], t, l))

    def calc_reachable_nodes(self, node, a, b):
        reach_num = 1
        min_at = [np.inf for i in range(len(self.nodelist))]
        min_at[node] = 0
        for (u, v, t, l) in self.edgelist:
            if t < a or t + l > b: continue
            if min_at[u] <= t:
                if min_at[v] > t + 1:
                    min_at[v] = t + 1
                    reach_num = reach_num + 1
        return reach_num

    def calc_total_reachability(self, a, b):
        total_reach = 0
        for x in self.nodelist:
            total_reach = total_reach + self.calc_reachable_nodes(x, a, b)
        return total_reach

    def total_reachability_after(self, node, a, b):
        after = 0
        for x in self.nodelist:
            reach_num = 1
            if x == node:
                reach_num = 0
            min_at = [np.inf for i in range(len(self.nodelist))]
            min_at[x] = 0
            for (u, v, t, l) in self.edgelist:
                if u != node and v != node:
                    if t < a or t + l > b: continue
                    if min_at[u] <= t:
                        if min_at[v] > t + 1:
                            min_at[v] = t + 1
                            reach_num = reach_num + 1
            after = after + reach_num
        return after

    def inner(self, a, b, node, my_heap):
        R = 0
        for x in self.nodelist:
            reach_num = 1
            if x == node:
                reach_num = 0
            min_at = [np.inf for i in range(len(self.nodelist))]
            min_at[x] = 0
            for (u, v, t, l) in self.edgelist:
                if u != node and v != node:
                    if t < a or t + l > b: continue
                    if min_at[u] <= t:
                        if min_at[v] > t + 1:
                            min_at[v] = t + 1
                            reach_num = reach_num + 1
            R = R + reach_num
            if my_heap != [] and -R < my_heap[0][0]:
                return -1
        return R

    def top_k_nodes(self, a, b, k):
        start_time = time.time()
        my_heap = []
        for node in self.nodelist:
            R = self.inner(a, b, node, my_heap)
            if R == -1:
                continue
            if len(my_heap) < k:
                heapq.heappush(my_heap, (-R, node))
            else:
                if -R > my_heap[0][0]:
                    heapq.heappushpop(my_heap, (-R, node))
        return my_heap, ("--- finished in %s seconds ---" % (time.time() - start_time))


if __name__ == '__main__':
    # data = input('Edgeliste eingeben: ')
    data = 'tij_SFHH.txt'
    output = data.split(".")[0] + '_Ranking' + '.txt'
    G = TemporalGraph({}, [])
    G.import_edgelist(data)
    print(G.top_k_nodes(0, np.inf, 4))
    # aves-weaver-social.edges, test1.txt
