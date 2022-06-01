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
    convert('/edge-lists/help1.txt', '/edge-lists/tij_SFHH2.txt')
    # swap('/edge-lists/help.txt', '/edge-lists/help1.txt')


    # DATASETS:
    # /edge-lists/wiki_talk_nl.txt          |  |V| = 225.749 | |E| = 1.554.698
    # /edge-lists/wikipediasg.txt           |  |V| = 208.142 | |E| = 810.702
    # /edge-lists/facebook.txt              |  |V| = 63.731  | |E| = 817.035
    # /edge-lists/infectious.txt            |  |V| = 10.972  | |E| = 415.912    234.7 min
    # /edge-lists/ia-contacts_dublin.txt    |  |V| = 10.972  | |E| = 415.912
    # /edge-lists/copresence-InVS13.txt     |  |V| = 95      | |E| = 394.247
    # /edge-lists/ia-reality-call.txt       |  |V| = 6.809   | |E| = 52.050
    # /edge-lists/ht09_contact_list.txt     |  |V| = 5.351   | |E| = 20.817     2.727 min
    # /edge-lists/twitter.txt               |  |V| = 4.605   | |E| = 23.736     352.0 min
    # /edge-lists/tij_SFHH.txt              |  |V| = 3.906   | |E| = 70.261     2.870 min
    # /edge-lists/fb-messages.txt           |  |V| = 1.899   | |E| = 61.734
    # /edge-lists/email-dnc.txt             |  |V| = 1.891   | |E| = 39.264     67.23 min
    # /edge-lists/fb-forum.txt              |  |V| = 899     | |E| = 33.720
    # reptilia-tortoise-network-fi.txt      |  |V| = 787     | |E| = 1.713
    # /edge-lists/aves-weaver-social.txt    |  |V| = 445     | |E| = 1.426      0.022 min
    # /edge-lists/example_graph1.txt        |  |V| = 7       | |E| = 18         0.005 min
    # /edge-lists/example_graph2.txt        |  |V| = 7       | |E| = 9          0.005 min