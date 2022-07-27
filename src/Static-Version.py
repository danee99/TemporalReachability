import multiprocessing
import os

path = os.path.join(os.getcwd(), os.pardir) + "\\edge-lists\\"


class StaticGraph:
    def __init__(self):
        self.n = 0
        self.m = 0
        self.graph = {}
        self.total_reachability = 0

    def add_edge(self, u, v):
        if u not in self.graph:
            self.graph[u] = set()
        if v not in self.graph:
            self.graph[v] = set()
        self.graph[u].add(v)
        self.graph[v].add(u)

    def import_edgelist(self, file_name):
        with open(path + file_name, "r") as f:
            self.n = int(f.readline())
            for line in f:
                arr = line.split()
                u = int(arr[0])
                v = int(arr[1])
                self.add_edge(u, v)

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

    # ranks the node x
    def rank_node(self, x):
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
        return total, x

    def static_node_ranking(self):
        pool = multiprocessing.Pool(multiprocessing.cpu_count())
        result_objects = [pool.apply_async(self.rank_node, args=(node,)) for node in range(0, self.n)]
        ranking = [r.get() for r in result_objects]
        pool.close()
        pool.join()
        ranking.sort()
        print(ranking)


if __name__ == '__main__':
    G = StaticGraph()
    input_graph = input('Edgeliste eingeben:')
    G.import_directed_edgelist(input_graph)
    G.static_node_ranking()
