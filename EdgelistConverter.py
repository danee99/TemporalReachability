import os


def convert(file_name, output):
    nodemanager = {}
    with open(os.getcwd() + output, "w") as o:
        with open(os.getcwd() + file_name, "r") as f:
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
                o.write((str(nodemanager[u]) + " " + str(nodemanager[v]) + " " + str(t) + " " + str(l) + "\n"))
                o.write((str(nodemanager[v]) + " " + str(nodemanager[u]) + " " + str(t) + " " + str(l) + "\n"))
        o.write(str(len(nodemanager.keys())))


def betw(file_name, output):
    nodemanager = {}
    with open(os.getcwd() + output, "w") as o:
        with open(os.getcwd() + file_name, "r") as f:
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


if __name__ == '__main__':
    # convert('/edge-lists/example_graph2.txt', '/edge-lists/example_graph.txt')
    inp = input('Edgeliste eingeben:')
    file_in = '/edge-lists/' + str(inp)
    file_out ='/edge-lists/' + '0_'+str(inp)
    convert(file_in, file_out)
