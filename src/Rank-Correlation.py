import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
import scipy.stats as stats
from numpy import loadtxt

path = "C:\\Users\\Daniel\\Documents\\GitHub\\TemporalReachability\\"
# path = "/home/stud/degenste/BA/TemporalReachability"


def import_ranking(degree_input, reachability_input, output_name, number_of_nodes, betw_input, close_input):
    arr3 = []
    arr4 = [0 for _ in range(0,number_of_nodes)]
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


mydataframe = pd.read_csv(path + "/Dataframes/UC-Irvine-messages")
obj = sns.heatmap(data=mydataframe.corr(method='kendall'), annot=True)
obj.set_xticklabels(obj.get_xticklabels(), rotation=90)
plt.tight_layout()
plt.savefig(path + '/Plots/UC-Irvine-messages.svg')

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
