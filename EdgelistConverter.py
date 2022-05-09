def convert(file_name, output):
    file = 'edge-lists\\' + file_name
    out = 'edge-lists\\' + output + '.txt'
    nodemanager = {}
    edgelist = []
    with open(file) as fp:
        with open(out, 'w') as f:
            val = 0
            for line in fp:
                arr = line.split()
                u = int(arr[0])
                v = int(arr[1])
                t = int(arr[2])
                try:
                    l = int(arr[3])
                except IndexError:
                    l = 1
                if u not in nodemanager.keys():
                    nodemanager.update({u: val})
                    val = val + 1
                if v not in nodemanager.keys():
                    nodemanager.update({v: val})
                    val = val + 1
                f.write(str(nodemanager[u]) + " " + str(nodemanager[v]) + " " + str(t) + " " + str(l) + "\n")
            f.write(str(len(nodemanager.values())))


if __name__ == '__main__':
    convert('wikipediasg.tg2', 'wikipediasg')