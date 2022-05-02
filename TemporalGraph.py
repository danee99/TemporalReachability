import heapq
import time

import numpy as np


class TemporalGraph:
    def __init__(self, nodelist, edgelist):
        self.nodelist = {}
        # self.outdegree = []
        self.edgelist = []

    # outputs the set of nodes and every temporal edge
    def print_graph(self):
        for i in self.edgelist:
            print(*i)
        print(self.nodelist)
        # print(self.outdegree)

    # Assumption: Input graph is in edge stream representation, i.e. edges are sorted by timestamps
    def import_edgelist(self, file_name):
        with open('edge-lists\\' + file_name, "r") as f:
            # self.outdegree = []
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
                    self.nodelist.update({u: 0})
                    # self.nodelist.append(u)
                    # self.outdegree.append(0)
                if v not in self.nodelist:
                    self.nodelist.update({v: 0})
                    # self.nodelist.append(v)
                    # self.outdegree.append(0)
                # self.outdegree[u] = self.outdegree[u] + 1
                self.nodelist[u] = self.nodelist[u] + 1
                self.edgelist.append((u, v, t, l))
        self.nodelist = {k: v for k, v in sorted(self.nodelist.items(), key=lambda item: item[1], reverse=True)}

    # O(n+m)
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

    # O(n^2 + nm)
    def total_reachability(self, a, b):
        result = []
        for node in self.nodelist:
            result.append(self.calc_reachable_nodes(node, a, b))
        # print(result)
        return sum(result)

    # calculates the total reachability of the entire graph after deleting "node"
    def total_reachability_after(self, a, b, node, my_heap, k):
        result = 0
        count = 0
        for x in self.nodelist.keys():
            count = count + 1
            reach_num = 1
            if x == node:
                reach_num = 0
            min_at = [np.inf for i in range(0, len(self.nodelist))]
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
                if -result < my_heap[0][0]:
                    return -1
        return result

    # outputs the top k nodes
    def top_k_nodes(self, a, b, k):
        start_time = time.time()
        my_heap = []
        for node in self.nodelist.keys():
            R = self.total_reachability_after(a, b, node, my_heap, k)
            if R == -1:
                continue
            if len(my_heap) < k:
                heapq.heappush(my_heap, (-R, node))
            else:
                if -R > my_heap[0][0]:
                    heapq.heappushpop(my_heap, (-R, node))
        return my_heap, ("--- finished in %s seconds ---" % (time.time() - start_time))
    # -------------------------------------------------------------------------------------------------------------------
    def total_reachability(self, a, b):
        total_reach = 0
        for x in self.nodelist:
            reach_num = 1
            min_at = [np.inf for i in range(0, len(self.nodelist))]
            min_at[x] = 0
            for (u, v, t, l) in self.edgelist:
                if t < a or t + l > b: continue
                if min_at[u] <= t:
                    if min_at[v] > t + 1:
                        min_at[v] = t + 1
                        reach_num = reach_num + 1
            total_reach = total_reach + reach_num
        return total_reach

    def rank_node(self, a, b, node, before):
        after = 0
        for x in self.nodelist:
            reach_num = 1
            if x == node:
                reach_num = 0
            min_at = [np.inf for i in range(0, len(self.nodelist))]
            min_at[x] = 0
            for (u, v, t, l) in self.edgelist:
                if u != node and v != node:
                    if t < a or t + l > b: continue
                    if min_at[u] <= t:
                        if min_at[v] > t + 1:
                            min_at[v] = t + 1
                            reach_num = reach_num + 1
            after = after + reach_num
        return 1 - (after / before)

    def rank_all_nodes(self, a, b, output_name):
        start_time = time.time()
        h = self.total_reachability(a, b)
        new_list = []
        for i in self.nodelist:
            new_list.append((i, self.rank_node(a, b, i, h)))
        new_list.sort(key=lambda y: y[1], reverse=True)
        with open('edge-lists\\' + output_name, 'w') as f:
            for rank in new_list:
                f.write(str(rank[0]) + ' ' + str(rank[1]) + "\n")
            f.write("--- finished in %s seconds ---" % (time.time() - start_time))


if __name__ == '__main__':
    # data = input('Edgeliste eingeben: ')
    data = 'aves-weaver-social.txt'
    output = data.split(".")[0] + '-Ranking' + '.txt'
    G = TemporalGraph([], [])
    G.import_edgelist(data)
    a = 0
    b = np.inf
    print(G.top_k_nodes(a, b, 3))
    # wikipediasg.txt         |  V = 208142 | E = 810702    geschätzt 6 h nur um gesamterreichbarkeit auszurechnen
    # facebook.txt            |  V = 63731  | E = 817036
    # infectious.txt          |  V = 10972  | E = 415912
    # tij_SFHH.txt            |  V = 3906   | E = 70261     1.3 knoten pro minute --> 50 h
    # ht09_contact_list.txt   |  V = 5351   | E = 20817     3 knoten pro minute --> 29 h
    # aves-weaver-social.txt  |  V = 445    | E = 1426
    # test.txt                |  V = 7      | E = 18