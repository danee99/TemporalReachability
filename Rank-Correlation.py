import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os


def import_ranking(degree_input, reachability_input, output_name, number_of_nodes, betweenness_input):
    with open(os.getcwd() + output_name, 'w') as f:
        f.write("Degree Centrality,Reachability Centrality\n")
        with open(os.getcwd() + degree_input, "r") as a:
            with open(os.getcwd() + reachability_input, "r") as b:
                line1 = a.readlines()
                line2 = b.readlines()
                arr1 = np.fromstring(line1[0].strip('[]\n'), dtype=float, sep=',')
                arr2 = np.fromstring(line2[0].strip('[]\n'), dtype=float, sep=',')
                for j in range(0, number_of_nodes):
                    f.write(str(j) + "," + str(arr1[j]) + "," + str(arr2[j]) + '\n')


# mydataframe = pd.read_csv(os.getcwd() + "/Dataframes/email-dnc")
# sns.heatmap(data=mydataframe.corr(method='kendall'))
# plt.show()

name = "aves-weaver-social"
import_ranking("/edge-lists/Degree Centrality/" + name + "-Outdegrees.txt",
               "/edge-lists/" + name + "-Rangliste.txt",
               "/Dataframes/" + name,
               445,
               "/edge-lists/Temporal Betweenness Centrality/" + name + "-Outdegrees.txt")