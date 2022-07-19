import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

path = os.path.join(os.getcwd(), os.pardir)


def import_ranking(degree_input, reachability_input, output_name, number_of_nodes):
    with open(path + "\\Dataframes\\" + output_name, 'w') as f:
        f.write("Degree Centrality,Reachability Centrality\n")
        with open(path + "\\Rankings\\Degree Centrality\\" + degree_input, "r") as a:
            with open(path + "\\Rankings\\Temporal Reachability\\" + reachability_input, "r") as b:
                line1 = a.readlines()
                line2 = b.readlines()
                arr1 = np.fromstring(line1[0].strip('[]\n'), dtype=float, sep=',')
                arr2 = np.fromstring(line2[0].strip('[]\n'), dtype=float, sep=',')
                print(arr1)
                print(arr2)
                # for j in range(0, number_of_nodes):
                #     f.write(str(j) + "," + str(arr1[j]) + "," + str(arr2[j]) + '\n')


# mydataframe = pd.read_csv(os.getcwd() + "/Dataframes/email-dnc")
# sns.heatmap(data=mydataframe.corr(method='kendall'))
# plt.show()

name = "ia-workplace-contacts"
import_ranking(name + "-Outdegrees.txt",
               name + "-Ranking.txt",
               name,
               92)
