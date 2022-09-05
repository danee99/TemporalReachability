import os
import numpy as np
from matplotlib import pyplot as plt
import networkx as nx

path = os.path.join(os.getcwd(), os.pardir) + "\\edge-lists\\"

# name = "Auswirkungen-der-Modifikationen"
# bar_width = 0.25
# x = ['radoslaw-email\nk = 1, Tiefe = 5', 'email-dnc\nk = 2, Tiefe = 5', 'UC-Irvine-messages\nk = 2, Tiefe = 5', 'dblp-cite\nk = 2, Tiefe = 1', 'wiki_talk_gl\nk = 1, Tiefe = 2']
# heuristik = [0.3, 3.6, 23.3, 5.1, 19.76]
# normal = [0.34, 9.9, 32.4, 42.8, 219.6]
# k_neighborhood = [0.24, 2.3, 9.26, 18.23, 10.74]
# bar1 = np.arange(len(x))
# bar2 = [i + bar_width for i in bar1]
# bar3 = [i + bar_width for i in bar2]
# plt.grid(linestyle='dashed')
# plt.bar(bar1, normal, bar_width, label="Knoten-Ranking", edgecolor='black')
# plt.bar(bar2, heuristik, bar_width, label="Heuristik", edgecolor='black')
# plt.bar(bar3, k_neighborhood, bar_width, label="k Nachbarschaft", edgecolor='black')
# plt.xlabel("\nDatensätze", fontsize=11)
# plt.ylabel("Laufzeit in min", fontsize=11)
# plt.title("Auswirkungen der Heuristik und der Modifikation auf die Laufzeit", fontsize=11)
# plt.xticks([r + bar_width for r in range(len(bar1))], x)
# plt.legend()
# for i, v in enumerate(heuristik):
#     plt.text(i + 0.14, 0 / heuristik[i] + heuristik[i] + 1, heuristik[i], fontsize=10)
# for i, v in enumerate(normal):
#     plt.text(i - 0.2, 0 / normal[i] + normal[i] + 1, normal[i], fontsize=10)
# for i, v in enumerate(k_neighborhood):
#     if i == 0:
#         plt.text(i + 0.45, 0 / k_neighborhood[i] + k_neighborhood[i] + 2, k_neighborhood[i], fontsize=10)
#     else:
#         plt.text(i + 0.45, 0 / k_neighborhood[i] + k_neighborhood[i] + 1, k_neighborhood[i], fontsize=10)
# plt.tight_layout()
# plt.savefig(os.path.join(os.getcwd(), os.pardir) + '\\Plots\\' + name + '.svg')
# plt.show()

datasets = ["fb-forum\nmit k = 2", "fb-messages\nmit k = 2", "twitter\nmit k = 3", "infectious\nmit k = 3", "ia-reality-call\nmit k = 3"]
n_groups = 5
normal = [2.44, 32.9, 104.1, 213.5, 962.1]
k_neighborhood = [1.1, 9.3, 8.2, 163.1, 39.6]
fig, ax = plt.subplots()
index = np.arange(n_groups)
bar_width = 0.35
opacity = 0.8
rects1 = plt.bar(index, normal, bar_width, edgecolor='black',
label='Knoten-Ranking')
rects2 = plt.bar(index + bar_width, k_neighborhood, bar_width, edgecolor='black',
color='g',
label='k-Nchbarschaft')
plt.grid(linestyle='dashed')
plt.xlabel('\nDatensätze')
plt.ylabel('Laufzeit in Minuten')
plt.title('Auswirkung der k-Nachbarschaftsmodifikation auf die Laufzeit')
plt.xticks(index + bar_width, datasets)
plt.legend()
for i, v in enumerate(normal):
    plt.text(i - 0.21, 0 / normal[i] + normal[i] + 2, normal[i], fontsize=11)
for i, v in enumerate(k_neighborhood):
    plt.text(i + 0.25, 0 / k_neighborhood[i] + k_neighborhood[i] + 2, k_neighborhood[i], fontsize=11)
plt.tight_layout()
plt.show()

# print(plt.style.available)
# plt.style.use('bmh')
# nodes_x_val = [445, 1891, 4605, 3906, 5351, 10972]
# edges_x_val = [1426, 39264, 23736, 70261, 20817, 415912]
# y_val = [0, 67, 402, 2, 3, 235]
# # in minutes
# plt.plot(edges_x_val, y_val, 'o')
# plt.xlabel("Anzahl Kanten")
# plt.ylabel("Laufzeit")
# plt.title("Abhängigkeit von Knotenanzahl")
# plt.grid(True)
# plt.tight_layout()
# plt.show()


# def draw_graph(file_name):
#     G = nx.Graph()
#     file = path + file_name
#     with open(file) as fp:
#         nothing_important = int(fp.readline())
#         for line in fp:
#             arr = line.split()
#             u = arr[0]
#             v = arr[1]
#             t = arr[2]
#             G.add_edge(int(u), int(v), weight=t)
#     pos = nx.spring_layout(G)
#     weights = nx.get_edge_attributes(G, "weight")
#     nx.draw_networkx(G, pos, with_labels=True)
#     nx.draw_networkx_edge_labels(G, pos, edge_labels=weights)
#     plt.show()
#
#
# draw_graph("example_graph3.txt")
