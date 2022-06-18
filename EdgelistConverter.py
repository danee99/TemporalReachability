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
                o.write((str(nodemanager[u]) + " " + str(nodemanager[v]) + " " + str(t) + " " + str(l) + "\n"))
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
                u = int(arr[0])
                v = int(arr[1])
                l = int(arr[2])
                t = int(arr[3])
                o.write((str(u) + " " + str(v) + " " + str(t) + " " + str(l) + "\n"))


if __name__ == '__main__':
    # convert('/edge-lists/example_graph2.txt', '/edge-lists/example_graph.txt')
    inp = input('Edgeliste eingeben:')
    file_in = '/edge-lists/' + str(inp)
    file_out ='/edge-lists/' + '0_'+str(inp)
    betw(file_in, file_out)
    # DATASETS:                                                                 Node Ranking | Top k  | Heuristik (k-core)
    # wiki_talk_nl.txt                      |  |V| = 225.749 | |E| = 1.554.698
    # wikipediasg.txt                       |  |V| = 208.142 | |E| = 810.702
    # facebook.txt                          |  |V| = 63.731  | |E| = 817.035
    # twitter.txt                           |  |V| = 4.605   | |E| = 23.736     352.0 min | 392.4 min | 393.5 min (1-core) --> 64.09 min (2-core)
    # ia-reality-call.txt                   |  |V| = 6.809   | |E| = 52.050     307.1 min | 343.0 min | 107.3 min (1-core) geloeschte Knoten Anzahl: 3209
    # infectious.txt                        |  |V| = 10.972  | |E| = 415.912    234.7 min | 230.4 min | 191.51 min (1-core) gelöschte Knoten Anzahl: 1296
    # ia-contacts_dublin.txt                |  |V| = 10.972  | |E| = 415.912    185.8 min | 230.5 min | 194.25 min (1-core) geloeschte Knoten Anzahl: 1296
    # fb-messages.txt                       |  |V| = 1.899   | |E| = 61.734     125.3 min |       min | 146.44 min (2-core) geloeschte Knoten Anzahl: 562
    # email-dnc.txt                         |  |V| = 1.891   | |E| = 39.264     67.23 min | 66.62 min | 26.14 min (1-core) gelöschte Knoten Anzahl: 912
    # copresence-InVS15.txt                 |  |V| = 219     | |E| = 1.283.194  11.76 min |       min |
    # fb-forum.txt                          |  |V| = 899     | |E| = 33.720     9.164 min | 12.03 min | 7.557 min (2-core)
    # tij_SFHH.txt                          |  |V| = 403     | |E| = 70.261     5.790 min | 10.63 min | 10.23 min (1-core) --> gelöschte Knoten Anzahl: 7
    # ht09_contact_list.txt                 |  |V| = 5.351   | |E| = 20.817     2.727 min | 2.701 min | 0.0005 min (1-core) --> gelöschte Knoten Anzahl: Alle
    # copresence-InVS13.txt                 |  |V| = 95      | |E| = 394.247    0.771 min | 1.235 min | 0.947 min --> gelöschte Knoten Anzahl: 1
    # reptilia-tortoise-network-fi.txt      |  |V| = 787     | |E| = 1.713      0.053 min | 0.036 min | 0.009 min --> gelöschte Knoten Anzahl: 584
    # aves-weaver-social.txt                |  |V| = 445     | |E| = 1.426      0.022 min | 0.013 min | 0.006 min --> gelöschte Knoten Anzahl 366

