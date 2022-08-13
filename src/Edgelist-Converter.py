import os

path = os.path.join(os.getcwd(), os.pardir) + "\\edge-lists\\"


def convert(file_name, output):
    nodemanager = {}
    with open(path + output, "w") as o:
        with open(path + file_name, "r") as f:
            n = int(f.readline())
            id = 0
            for line in f:
                arr = line.split()
                u = int(arr[0])
                v = int(arr[1])
                t = int(arr[2])
                try:
                    l = int(arr[3])
                except IndexError:
                    l = 1
                if u not in nodemanager.keys():
                    nodemanager[u] = id
                    id = id + 1
                if v not in nodemanager.keys():
                    nodemanager[v] = id
                    id = id + 1
                o.write((str(nodemanager[u]) + " " + str(nodemanager[v]) + " " + str(t) + " " + str(1) + "\n"))
                # o.write((str(nodemanager[v]) + " " + str(nodemanager[u]) + " " + str(t) + " " + str(l) + "\n"))
        o.write(str(len(nodemanager.keys())))


def convert2(file_name, output):
    nodemanager = {}
    E = []
    with open(path + file_name, "r") as f:
        # n = int(f.readline())
        id = 0
        for line in f:
            arr = line.split()
            u = int(arr[0])
            v = int(arr[1])
            t = int(arr[3])
            try:
                l = int(arr[2])
            except IndexError:
                l = 1
            if u not in nodemanager.keys():
                nodemanager[u] = id
                id = id + 1
            if v not in nodemanager.keys():
                nodemanager[v] = id
                id = id + 1
            E.append((nodemanager[u], nodemanager[v], t, l))
    E.sort(key=lambda tup: tup[2])
    with open(path + output, "w") as o:
        for (g, h, t, l) in E:
            o.write((str(g) + " " + str(h) + " " + str(t) + " " + str(l) + "\n"))
        o.write(str(len(nodemanager)))


def betw(file_name, output):
    with open(path + output, "w") as o:
        with open(path + file_name, "r") as f:
            int(f.readline())
            for line in f:
                arr = line.split()
                u = int(arr[0])
                v = int(arr[1])
                t = int(arr[2])
                o.write((str(u) + " " + str(v) + " " + str(t) + "\n"))


def closeness(file_name, output):
    with open(path + output, "w") as o:
        with open(path + file_name, "r") as f:
            n = int(f.readline())
            o.write((str(n) + "\n"))
            for line in f:
                arr = line.split()
                u = int(arr[0])
                v = int(arr[1])
                t = int(arr[2])
                l = int(arr[3])
                o.write((str(u) + " " + str(v) + " " + str(t) + " " + str(l) + "\n"))
                # o.write((str(v) + " " + str(u) + " " + str(t) + " " + str(l) + "\n"))

def swap(file_name, output):
    with open(os.getcwd() + output, "w") as o:
        with open(os.getcwd() + file_name, "r") as f:
            for line in f:
                arr = line.split()
                t = int(arr[0])
                u = int(arr[1])
                v = int(arr[2])
                l1 = arr[3]
                l2 = arr[4]
                o.write((str(u) + " " + str(v) + " " + str(t) + " " + str(1) + "\n"))


def fail(file_name, output):
    # E = []
    # edge_before = (-1, -1, -1, -1)
    # with open(path + file_name, "r") as f:
    #     f.readline()
    #     for line in f:
    #         arr = line.split()
    #         u = int(arr[0])
    #         v = int(arr[1])
    #         t = int(arr[2])
    #         l = int(arr[3])
    #         l_h = edge_before[3]
    #         if edge_before[0] == u and edge_before[1] == v and edge_before[2] + edge_before[3] == t:
    #             l_h += l
    #             E.remove(edge_before)
    #             E.append((u, v, edge_before[2], l_h))
    #             edge_before = (u, v, edge_before[2], l_h)
    #         else:
    #             edge_before = (u, v, t, l)
    #             E.append((u, v, t, l))
    #     with open(path + output, "w") as o:
    #         for (u, v, t, l) in E:
    #             o.write((str(u) + " " + str(v) + " " + str(t) + " " + str(l) + "\n"))
    with open(path + file_name, "r") as f:
        f.readline()
        with open(path + output, "w") as o:
            for line in f:
                arr = line.split()
                u = int(arr[0])
                v = int(arr[1])
                t = int(arr[2])
                l = int(arr[3])
                o.write((str(u) + " " + str(v) + " " + str(t - 20) + " " + str(20) + "\n"))


def fail2(file_name, output):
    E = {}
    edges = []
    # {(u,v) : [t, l]}
    with open(path + file_name, "r") as f:
        f.readline()
        for line in f:
            arr = line.split()
            u = int(arr[0])
            v = int(arr[1])
            t = int(arr[2])
            l = int(arr[3])
            if (u, v) not in E:
                E[(u, v)] = [t, l]
                edges.append((u, v, E[(u, v)][0], E[(u, v)][1]))
            else:
                if E[(u, v)][0] + E[(u, v)][1] == t:
                    edges.remove((u, v, E[(u, v)][0], E[(u, v)][1]))
                    E[(u, v)][1] += l
                    edges.append((u, v, E[(u, v)][0], E[(u, v)][1]))
                else:
                    E[(u, v)] = [t, l]
                    edges.append((u, v, E[(u, v)][0], E[(u, v)][1]))
        with open(path + output, "w") as o:
            for (u, v, t, l) in edges:
                o.write((str(u) + " " + str(v) + " " + str(t) + " " + str(l) + "\n"))


if __name__ == '__main__':
    # convert('wiki_talklv.txt', 'wiki_talk_lv.txt')
    # convert('wiki_talk_el.txt', 'wiki_talk_elr.txt')
    betw('wiki_talk_gl.txt', 'B_wiki_talk_gl.txt')
    # inp = input('Edgeliste eingeben:')
    # file_in = '/edge-lists/' + str(inp)
    # file_out ='/edge-lists/' + '0_'+str(inp)
    # convert(file_in, file_out)
