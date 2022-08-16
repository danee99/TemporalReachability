import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
import scipy.stats as stats
from numpy import loadtxt
from sklearn.metrics import jaccard_score

path = "C:\\Users\\Daniel\\Documents\\GitHub\\TemporalReachability\\"


# path = "/home/stud/degenste/BA/TemporalReachability"


def import_ranking(degree_input, reachability_input, output_name, number_of_nodes, betw_input, close_input):
    arr3 = []
    arr4 = [0 for _ in range(0, number_of_nodes)]
    with open(path + "Dataframes\\" + output_name, 'w') as f:
        f.write("Degree Centrality,Reachability Centrality,Temporal Betweenness,Temporal Closeness\n")
        with open(path + "Rankings\\Degree Centrality\\" + degree_input, "r") as a:
            with open(path + "Rankings\\Temporal Reachability\\" + reachability_input, "r") as b:
                with open(path + "Rankings\\Temporal Betweenness Centrality\\" + betw_input, "r") as c:
                    with open(path + "Rankings\\Temporal Closeness\\" + close_input, "r") as d:
                        for line in c:
                            arr = line.split(",")
                            betw_rank = float(arr[1])
                            if betw_rank < 0:
                                arr3.append(0)
                            else:
                                arr3.append(betw_rank)
                        for line in d:
                            arr = line.split(",")
                            close_rank = float(arr[1])
                            corresponding_node = int(arr[0])
                            arr4[corresponding_node] = close_rank
                    line1 = a.readlines()
                    line2 = b.readlines()
                    arr1 = np.fromstring(line1[0].strip('[]\n'), dtype=float, sep=',')
                    arr2 = np.fromstring(line2[0].strip('[]\n'), dtype=float, sep=',')
                    for j in range(0, number_of_nodes):
                        f.write(str(j) + "," + str(arr1[j]) + "," + str(arr2[j]) + "," + str(arr3[j]) + "," +
                                str(arr4[j]) + '\n')


def import_ranking_alternative(degree_input, reachability_input, output_name, number_of_nodes, betw_input, close_input,
                               static_input, static_degree_input):
    arr3 = []
    arr4 = []
    with open(path + "Dataframes\\" + output_name, 'w') as g:
        g.write(
            "Temp. Reachability,Stat. Reachability,Temp. Betweenness,Temp. Closeness,Degree Centrality,Stat. Degree\n")
        with open(path + "Rankings\\Degree Centrality\\" + degree_input, "r") as a:
            with open(path + "Rankings\\Degree Centrality\\" + static_degree_input, "r") as f:
                with open(path + "Rankings\\Temporal Reachability\\" + reachability_input, "r") as b:
                    with open(path + "Rankings\\Temporal Betweenness Centrality\\" + betw_input, "r") as c:
                        with open(path + "Rankings\\Temporal Closeness\\" + close_input, "r") as d:
                            with open(path + "Rankings\\Static Reachability\\" + static_input, "r") as e:
                                for line in c:
                                    arr = line.split(",")
                                    betw_rank = float(arr[1])
                                    if betw_rank < 0:
                                        arr3.append(0)
                                    else:
                                        arr3.append(betw_rank)
                                for line in d:
                                    arr = line.split(",")
                                    close_rank = float(arr[1])
                                    if close_rank < 0:
                                        arr4.append(0)
                                    else:
                                        arr4.append(close_rank)
                                line1 = a.readlines()
                                line2 = b.readlines()
                                line5 = e.readlines()
                                line6 = f.readlines()
                                arr1 = np.fromstring(line1[0].strip('[]\n'), dtype=float, sep=',')
                                arr2 = np.fromstring(line2[0].strip('[]\n'), dtype=float, sep=',')
                                arr5 = np.fromstring(line5[0].strip('[]\n'), dtype=float, sep=',')
                                arr6 = np.fromstring(line6[0].strip('[]\n'), dtype=float, sep=',')
                                for j in range(0, number_of_nodes):
                                    g.write(
                                        str(j) + "," + str(arr2[j]) + "," + str(arr5[j]) + "," + str(arr3[j]) + "," +
                                        str(arr4[j]) + "," + str(arr1[j]) + "," + str(arr6[j]) + '\n')


# name = "UC-Irvine-messages"
# mydataframe = pd.read_csv(path + "/Dataframes/"+name)
# mydataframe = mydataframe.rename(columns={'Temp. Reachability': 'Temporal\nReachability',
#                                           'Stat. Reachability': 'Static\nReachability',
#                                           'Temp. Betweenness': 'Temporal\nBetweenness',
#                                           'Temp. Closeness': 'Temporal\nCloseness',
#                                           'Degree Centrality': 'Temporal\nOutdegree',
#                                           'Stat. Degree': 'Static\nOutdegree'
#                                           })
# sns.set(font_scale=1.1)
# obj = sns.heatmap(data=mydataframe.corr(method='kendall'), annot=True, square=True, annot_kws={"size": 12}, linewidths=1)
# obj.set_xticklabels(obj.get_xticklabels(), rotation=90)
# plt.tight_layout()
# plt.savefig(path + '/Plots/'+name+'.svg')

top_k = 10
dataset = "radoslaw_email"
# with open(path + "edge-lists\\" + dataset + "-Heuristik-top-"+str(top_k)+".txt", "r") as h:
with open(path + "edge-lists\\" + dataset + "-k-Nachbarschaft-Ranking (Digraph)-top-" + str(top_k) + ".txt", "r") as h:
    with open(path + "edge-lists\\" + "radoslaw-email" + "-Ranking-top-"+str(top_k)+".txt", "r") as o:
        line1 = h.readlines()
        line2 = o.readlines()
        arr1 = np.fromstring(line1[0].strip('[]\n'), dtype=float, sep=',')
        arr2 = np.fromstring(line2[0].strip('[]\n'), dtype=float, sep=',')
        optimal = set(arr2)
        heuristik = set(arr1)
        print(len(optimal.intersection(heuristik)) / len(optimal.union(heuristik)))

# aves-weaver-social 445
# email-dnc 1891
# fb-forum 899
# fb-messages 1.899
# Haggle 274
# ia-hospital-ward-proximity-attr 75
# ia-workplace-contacts 92
# radoslaw_email 167
# twitter 4605
# UC-Irvine-messages 1899

# name = "UC-Irvine-messages"
# import_ranking_alternative(name + "-Outdegrees.txt",
#                            name + "-Ranking.txt",
#                            name,
#                            1899,
#                            name + "-temporal-betweenness.txt",
#                            name + "-temporal-closeness.txt",
#                            name + "-Ranking (static).txt",
#                            name + "-Outdegrees-static.txt"
#                            )

# name = "UC-Irvine-messages"
# import_ranking(name + "-Outdegrees.txt",
#                name + "-Ranking.txt",
#                name,
#                1899,
#                name+"-temporal-betweenness.txt",
#                name+"-temporal-closeness.txt"
#                )

# def vs_heuristik(heuristik_input, reachability_input):
#     with open(path + heuristik_input, 'r') as h:
#         with open(path + reachability_input, "r") as r:
#             line1 = h.readlines()
#             line2 = r.readlines()
#             heuristik = np.fromstring(line1[0].strip('[]\n'), dtype=float, sep=',')
#             reachability = np.fromstring(line2[0].strip('[]\n'), dtype=float, sep=',')
#             tau, p_value = stats.kendalltau(reachability, heuristik)
#             print(tau)
#
#
# vs_heuristik("email-dnc-Heuristik.txt", "email-dnc-Ranking.txt")
