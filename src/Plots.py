import os
import numpy as np
from matplotlib import pyplot as plt
import networkx as nx

path = os.path.join(os.getcwd(), os.pardir) + "\\edge-lists\\"
name = "Auswirkungen-der-Modifikationen"

bar_width = 0.25
x = ['radoslaw-\nemail', 'email-dnc', 'UC-Irvine-\nmessages', 'dblp-cite', 'wiki_talk_\ngl']
heuristik = [0.61, 4.85, 29.1, 5.24, 19.76]
normal = [0.67, 12.15, 40.79, 44.29, 230.33]
k_neighborhood = [1.03, 15.32, 68.6, 44.68, 10.0]

bar1 = np.arange(len(x))
bar2 = [i + bar_width for i in bar1]
bar3 = [i + bar_width for i in bar2]

plt.grid(linestyle='dashed')

plt.bar(bar1, normal, bar_width, label="Knoten-Ranking", edgecolor='black')
plt.bar(bar2, heuristik, bar_width, label="Heuristik", edgecolor='black')
plt.bar(bar3, k_neighborhood, bar_width, label="k Nachbarschaft", edgecolor='black')

plt.xlabel("\nDatensätze", fontsize=11)
plt.ylabel("Laufzeit in min", fontsize=11)
plt.title("Auswirkungen der Heuristik auf die Laufzeit", fontsize=11)

plt.xticks([r + bar_width for r in range(len(bar1))], x)
plt.legend()

for i, v in enumerate(heuristik):
    plt.text(i + 0.14, 0 / heuristik[i] + heuristik[i] + 1, heuristik[i], fontsize=10)
for i, v in enumerate(normal):
    plt.text(i - 0.2, 0 / normal[i] + normal[i] + 1, normal[i], fontsize=10)
for i, v in enumerate(k_neighborhood):
    if i == 0:
        plt.text(i + 0.45, 0 / k_neighborhood[i] + k_neighborhood[i] + 2, k_neighborhood[i], fontsize=10)
    else:
        plt.text(i + 0.45, 0 / k_neighborhood[i] + k_neighborhood[i] + 1, k_neighborhood[i], fontsize=10)

plt.tight_layout()
plt.savefig(os.path.join(os.getcwd(), os.pardir) + '\\Plots\\' + name + '.svg')
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
