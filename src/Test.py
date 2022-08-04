import multiprocessing
import os
import time
import heapq
import numpy as np

# path = os.path.join(os.getcwd(), os.pardir) + "\\edge-lists\\"
path = "/home/stud/degenste/BA/TemporalReachability/edge-lists/"


def is_label_dominated(label, Q):
    for item in Q:
        if (label[1] < item[1] and label[0] >= item[0]) or (item[1] == label[1] and item[0] == label[0]):
            return False
    return True


class TemporalGraph:
    def __init__(self):
        self.nodes = set()
        self.incidence_list = []
        self.n = 0
        self.m = 0
        self.total_reachability = 0

    def import_edgelist(self, file_name):
        with open(path + file_name, "r") as f:
            n = int(f.readline())
            self.n = n
            self.incidence_list = [[] for _ in range(n)]
            for line in f:
                arr = line.split()
                u = int(arr[0])
                v = int(arr[1])
                t = int(arr[2])
                try:
                    l = int(arr[3])
                except IndexError:
                    l = 1
                self.nodes.add(u)
                self.nodes.add(v)
                self.incidence_list[u].append((u, v, t, l))
                self.m += 1

    def import_undirected_edgelist(self, file_name):
        with open(path + file_name, "r") as f:
            n = int(f.readline())
            self.n = n
            self.incidence_list = [[] for _ in range(n)]
            for line in f:
                arr = line.split()
                u = int(arr[0])
                v = int(arr[1])
                t = int(arr[2])
                try:
                    l = int(arr[3])
                except IndexError:
                    l = 1
                self.nodes.add(u)
                self.nodes.add(v)
                self.incidence_list[u].append((u, v, t, l))
                self.incidence_list[v].append((v, u, t, l))
                self.m += 2

    def label_setting_fastest_path_algorithm(self, u):
        Q = []
        heapq.heappush(Q, (0, 0, u))
        d = [np.inf for _ in range(self.n)]
        d[u] = 0
        F = set()
        Pi = [np.inf for _ in range(self.n)]
        while Q:
            (a, s, v) = heapq.heappop(Q)
            if v in F:
                d[v] = a - s
                F.add(v)
            for (v, w, t, l) in self.incidence_list[v]:
                if a <= t:
                    if (a, s, v) == (0, 0, u):
                        label = (t + l, t, w)
                    else:
                        label = (t + l, s, w)
                    # Entferne die labels aus Pi[w] und Q, die dominiert werden 2 * O(n) ?
                    # (a0, s0, v) dominiert (a, s, v) wenn s < s0 und a >= a0, oder s = s0 und a > a0
                    # if label is not dominated: O(n) ?
                    if is_label_dominated(label, Q) == False:
                        heapq.heappush(Q, label)
                        Pi[w].add(label)
        return d


if __name__ == '__main__':
    print("The Cake Is A Lie")
