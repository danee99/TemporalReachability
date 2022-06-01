import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os


def import_ranking(degree_input, reachability_input, output_name, number_of_nodes):
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


mydataframe = pd.read_csv(os.getcwd() + "/Dataframes/tij_SFHH")
sns.heatmap(data=mydataframe.corr(method='kendall'))
plt.show()

# name = "infectious"
# import_ranking("/edge-lists/" + name + "-Outdegrees.txt",
#                "/edge-lists/" + name + "-Rangliste.txt",
#                "/Dataframes/" + name,
#                10972)


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
