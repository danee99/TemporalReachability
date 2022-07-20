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
            E.append((nodemanager[u], nodemanager[v], t, l))
    E.sort(key=lambda tup: tup[2])
    with open(path + output, "w") as o:
        for (g, h, t, l) in E:
            o.write((str(g) + " " + str(h) + " " + str(t) + " " + str(l) + "\n"))
        o.write(str(len(nodemanager)))


def betw(file_name, output):
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
                o.write((str(nodemanager[u]) + " " + str(nodemanager[v]) + " " + str(t) + "\n"))


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
    E = []
    edge_before = (-1, -1, -1, -1)
    t_before = -1
    with open(path + file_name, "r") as f:
        f.readline()
        for line in f:
            arr = line.split()
            u = int(arr[0])
            v = int(arr[1])
            t = int(arr[2])
            l = int(arr[3])
            if edge_before[0] == u and edge_before[1] == v:
                if edge_before[2] + edge_before[3] == t:
                    # E.append((u, v, edge_before[2], t+(2*l)-t_before))
                    E.append((u, v, edge_before[2], t + l - t_before))
                    E.remove(edge_before)
            else:
                edge_before = (u, v, t, l)
                t_before = t
                E.append(edge_before)

        with open(path + output, "w") as o:
            for (u, v, t, l) in E:
                o.write((str(u) + " " + str(v) + " " + str(t) + " " + str(l) + "\n"))
    # with open(path + file_name, "r") as f:
    #     f.readline()
    #     with open(path + output, "w") as o:
    #         for line in f:
    #             arr = line.split()
    #             u = int(arr[0])
    #             v = int(arr[1])
    #             t = int(arr[2])
    #             l = int(arr[3])
    #             o.write((str(u) + " " + str(v) + " " + str(t - 20) + " " + str(20) + "\n"))


if __name__ == '__main__':
    # convert2('twitter.txt', 'testing.txt')
    # fail('tij (fail).txt', 'tij (good).txt')
    betw('email-dnc.txt', '0_email-dnc.txt')
    # inp = input('Edgeliste eingeben:')
    # file_in = '/edge-lists/' + str(inp)
    # file_out ='/edge-lists/' + '0_'+str(inp)
    # convert(file_in, file_out)
