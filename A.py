import heapq
import os
import time
import heapq_max
import numpy as np


class TemporalGraph:
    def __init__(self, nodelist, edgelist):
        self.nodelist = {}
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
                    self.nodelist[u] = 0
                if v not in self.nodelist:
                    self.nodelist[v] = 0
                self.nodelist[u] = self.nodelist[u] + 1
                self.edgelist.append((u, v, t, l))
        self.nodelist = {k: v for k, v in sorted(self.nodelist.items(), key=lambda item: item[1], reverse=True)}

    # calculates the total reachability of the entire graph after deleting "node"
    # this is the helper function for the top k nodes
    def total_reachability_after(self, a, b, node, max_heap, k, help_list, arr):
        reachabilities = []
        copyofnodes = self.nodelist.copy()
        count = 0
        total_reach2 = 0
        n = len(self.nodelist.keys())
        for x in self.nodelist.keys():
            # if max_heap != [] and len(max_heap) >= k:
            #     if sum(reachabilities) + sum(copyofnodes.values()) > max_heap[0][0]:
            #         print("Inner LOOP zur Berechnung von R(G-v) abgebrochen nach " + str(
            #             count) + " wegen Grenze = " + str(sum(reachabilities) + sum(copyofnodes.values())) + " > " + str(abs(max_heap[0][0])))
            #         print("--> Einsparung von " + str(len(self.nodelist) - count) + " Schleifen")
            #         arr.append(len(self.nodelist) - count)
            #         return
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
            count = count + 1
            reachabilities.append(reach_num)
            copyofnodes.pop(x)
            total_reach2 = total_reach2 + reach_num
            if max_heap != [] and len(max_heap) >= k:
                if total_reach2 > max_heap[0][0]:
                    print("Inner LOOP zur Berechnung von R(G-v) abgebrochen nach " + str(
                        count) + " Knoten weil R(G-v) = " + str(
                        sum(reachabilities) + sum(copyofnodes.values())) + " > " + str(abs(max_heap[0][0])))
                    print("--> Einsparung von " + str(len(self.nodelist) - count) + " Schleifen")
                    arr.append(len(self.nodelist) - count)
                    return
        total_reach = sum(reachabilities)
        if len(max_heap) < k:
            heapq_max.heappush_max(max_heap, (total_reach, node))
        else:
            if total_reach < max_heap[0][0]:
                heapq_max.heappushpop_max(max_heap, (total_reach, node))

    # outputs the max heap with the top k nodes
    def top_k_nodes(self, a, b, k, output_name):
        start_time = time.time()
        max_heap = []
        savings = []
        help_list = [np.inf for i in range(0, len(self.nodelist.keys()))]
        for node in self.nodelist.keys():
            print("\nbin bei knoten " + str(node))
            self.total_reachability_after(a, b, node, max_heap, k, help_list, savings)
        # with open(os.getcwd() + output_name, 'w') as f:
            # f.write(str(max_heap) + "\n")
            # finish = time.time() - start_time
            # f.write("--- finished in %s seconds ---" % (finish) + "\n")
            # f.write("--- finished in %s minutes ---" % ((finish) / 60) + "\n")
        print(str(max_heap) + "\n")
        print("Einsparung von " + str(sum(savings)) + "\n")
        finish = time.time() - start_time
        print("--- finished in %s seconds ---" % (finish) + "\n")
        print("--- finished in %s minutes ---" % ((finish) / 60) + "\n")


if __name__ == '__main__':
    data = input('Edgeliste eingeben: ')
    k = int(input('k eingeben: '))
    output = data.split(".")[0] + '-TOP-' + str(k) + '.txt'
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
