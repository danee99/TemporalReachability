import os

def convert(file_name, output):
    nodemanager = {}
    with open(os.getcwd() + output, "w") as o:
        with open(os.getcwd() + file_name, "r") as f:
            # n = int(f.readline())
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
                o.write((str(nodemanager[u])+" "+str(nodemanager[v])+" "+str(t)+" "+str(l)+"\n"))
        o.write(str(len(nodemanager.keys())))

def swap(file_name, output):
    with open(os.getcwd() + output, "w") as o:
        with open(os.getcwd() + file_name, "r") as f:
            for line in f:
                arr = line.split()
                u = int(arr[0])
                v = int(arr[1])
                l = int(arr[2])
                t = int(arr[3])
                o.write((str(u)+" "+str(v)+" "+str(t)+" "+str(l)+"\n"))

if __name__ == '__main__':
    # convert('/edge-lists/edit-enwikibooks.edges', '/edge-lists/edit-enwikibooks.txt')
    swap('/edge-lists/edit-enwikibooks.txt', '/edge-lists/edit-enwikibooksAAA.txt')
    # 46952
    # 133449