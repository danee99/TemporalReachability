import heapq
import math
import time
from io import StringIO
import numpy as np


def show_tree(tree, total_width=60, fill=' '):
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
        output.write(str((abs(n[0]), n[1])).center(col_width, fill))
        last_row = row
    print(output.getvalue())
    print('-' * total_width)
    return


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
        # for node in self.nodelist:
        #     self.nodelist[node] = self.calc_reachable_nodes(node, a, b)
        # self.nodelist = {k: v for k, v in sorted(self.nodelist.items(), key=lambda item: item[1], reverse=True)}
        result = []
        for node in self.nodelist:
            result.append(self.calc_reachable_nodes(node, a, b))
        sum(result)

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
                    print("Inner LOOP zur Berechnung von R(G-v) abgebrochen nach " + str(
                        count) + " Knoten weil R(G-v) = " + str(result) + " > " + str(abs(my_heap[0][0])))
                    return -1
        print("Inner LOOP abgeschlossen nach " + str(count) + " Knoten --> R(G-v) = " + str(result))
        return result

    # outputs the top k nodes
    def top_k_nodes(self, a, b, k):
        start_time = time.time()
        my_heap = []
        for node in self.nodelist.keys():
            show_tree(my_heap, total_width=60, fill=' ')
            print("finished in %s seconds" % (time.time() - start_time))
            print("\nbin bei knoten " + str(node)+" " + str(self.nodelist[node]))
            R = self.total_reachability_after(a, b, node, my_heap, k)
            if R == -1:
                print("--> Der Knoten " + str(node) + " gehört nicht zu top k" + " --> " + str(R))
                continue
            if len(my_heap) < k:
                heapq.heappush(my_heap, (-R, node))
            else:
                if -R > my_heap[0][0]:
                    heapq.heappushpop(my_heap, (-R, node))
        return my_heap, ("--- finished in %s seconds ---" % (time.time() - start_time))

    def eins(self, a, b, node, my_heap, k):
        result = 0
        count = 0
        completed = []
        reach = []
        for x in self.nodelist.keys():
            count = count + 1
            reach_num = 1
            booo = 0
            for key in self.nodelist.keys():
                if key not in completed:
                    booo = booo + self.nodelist[key]
            bound = sum(reach) + booo
            if my_heap != [] and len(my_heap) >= k:
                if -bound < my_heap[0][0]:
                    print("HIER abgebrochen nach " + str(
                        count) + " Knoten weil Bound = " + str(bound) + " > " + str(abs(my_heap[0][0])))
                    return -1
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

            reach.append(reach_num)
            completed.append(x)

            result = result + reach_num
            if my_heap != [] and len(my_heap) >= k:
                if -result < my_heap[0][0]:
                    print("Inner LOOP zur Berechnung von R(G-v) abgebrochen nach " + str(
                        count) + " Knoten weil R(G-v) = " + str(result) + " > " + str(abs(my_heap[0][0])))
                    return -1
        print("Inner LOOP abgeschlossen nach " + str(count) + " Knoten --> R(G-v) = " + str(result))
        return result

    def zwei(self, a, b, k):
        start_time = time.time()
        my_heap = []
        for node in self.nodelist.keys():
            show_tree(my_heap, total_width=60, fill=' ')
            print("\nbin bei knoten " + str(node)+" " + str(self.nodelist[node]))
            R = self.eins(a, b, node, my_heap, k)
            if R == -1:
                print("--> Der Knoten " + str(node) + " gehört nicht zu top k" + " --> " + str(R))
                continue
            if len(my_heap) < k:
                heapq.heappush(my_heap, (-R, node))
            else:
                if -R > my_heap[0][0]:
                    heapq.heappushpop(my_heap, (-R, node))
        return (my_heap, ("--- finished in %s seconds ---" % (time.time() - start_time)))


if __name__ == '__main__':
    # data = input('Edgeliste eingeben: ')
    data = 'ht09_contact_list.txt'
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
