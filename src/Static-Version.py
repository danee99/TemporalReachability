import multiprocessing
import os
import time

# path = os.path.join(os.getcwd(), os.pardir) + "\\edge-lists\\"
path = "/home/stud/degenste/BA/TemporalReachability/edge-lists/"


class StaticGraph:
    def __init__(self):
        self.n = 0
        self.m = 0
        self.graph = {}
        self.total_reachability = 0

    def import_undirected_edgelist(self, file_name):
        with open(path + file_name, "r") as f:
            self.n = int(f.readline())
            for line in f:
                arr = line.split()
                u = int(arr[0])
                v = int(arr[1])
                if u not in self.graph:
                    self.graph[u] = set()
                if v not in self.graph:
                    self.graph[v] = set()
                self.graph[u].add(v)

    def import_directed_edgelist(self, file_name):
        with open(path + file_name, "r") as f:
            self.n = int(f.readline())
            for line in f:
                arr = line.split()
                u = int(arr[0])
                v = int(arr[1])
                if u not in self.graph:
                    self.graph[u] = set()
                if v not in self.graph:
                    self.graph[v] = set()
                self.graph[u].add(v)
                self.graph[v].add(u)

    # calculate the number of reachable nodes of src
    def num_reachable_nodes(self, src):
        visited = set()
        visited.add(src)
        queue = [src]
        while queue:
            v = queue.pop(0)
            for neighbour in self.graph[v]:
                if neighbour not in visited:
                    visited.add(neighbour)
                    queue.append(neighbour)
        return len(visited)

    def calc_total_reachability(self):
        self.total_reachability = sum([self.num_reachable_nodes(i) for i in self.graph])
        return self.total_reachability

    def rank_node(self, x, before):
        total = 0
        for node in self.graph:
            if node == x:
                continue
            visited = set()
            visited.add(node)
            queue = [node]
            while queue:
                v = queue.pop(0)
                for neighbour in self.graph[v]:
                    if neighbour != x:
                        if neighbour not in visited:
                            visited.add(neighbour)
                            queue.append(neighbour)
            total += len(visited)
        return 1 - (total / before)

    def static_node_ranking(self, output_name):
        start_time = time.time()
        before = self.calc_total_reachability()
        pool = multiprocessing.Pool(multiprocessing.cpu_count())
        result_objects = [pool.apply_async(self.rank_node, args=(node, before)) for node in range(0, self.n)]
        ranking = [r.get() for r in result_objects]
        pool.close()
        pool.join()
        finish = time.time() - start_time
        with open(path + output_name, 'w') as f:
            # ranking.sort(reverse=True)
            # for i in range(len(ranking)):
            #     f.write(str(i+1)+".Platz: "+str(ranking[i][1]) + "\n")
            f.write(str(ranking) + "\n")
            f.write("R(G) = %s" % self.total_reachability + "\n")
            f.write("abgeschlossen in %s Minuten" % (finish / 60) + "\n")


if __name__ == '__main__':
    G = StaticGraph()
    input_graph = input('Edgeliste eingeben:')
    directed = (input('Soll die Kantenliste als gerichtet betrachtet werden? [y/n]:'))
    if directed == 'y':
        G.import_directed_edgelist(input_graph)
    elif directed == 'n':
        G.import_undirected_edgelist(input_graph)
    G.static_node_ranking(input_graph.split(".")[0] + '-Ranking (static)' + '.txt')
