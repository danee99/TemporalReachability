import numpy as np
from matplotlib import pyplot as plt

print(plt.style.available)
plt.style.use('bmh')
nodes_x_val = [445, 1891, 4605, 3906, 5351, 10972]
edges_x_val = [1426, 39264, 23736, 70261, 20817, 415912]
y_val = [0, 67, 402, 2, 3, 235]
# in minutes
plt.plot(edges_x_val, y_val, 'o')
plt.xlabel("Anzahl Kanten")
plt.ylabel("Laufzeit")
plt.title("Abhängigkeit von Knotenanzahl")
plt.grid(True)
plt.tight_layout()
plt.show()
# /edge-lists/wiki_talk_nl.txt          |  |V| = 225.749 | |E| = 1.554.698
# /edge-lists/wikipediasg.txt           |  |V| = 208.142 | |E| = 810.702
# /edge-lists/facebook.txt              |  |V| = 63.731  | |E| = 817.035
# /edge-lists/infectious.txt            |  |V| = 10.972  | |E| = 415.912    234.7 min
# /edge-lists/ia-contacts_dublin.txt    |  |V| = 10.972  | |E| = 415.912
# /edge-lists/copresence-InVS13.txt     |  |V| = 95      | |E| = 394.247
# /edge-lists/ia-reality-call.txt       |  |V| = 6.809   | |E| = 52.050
# /edge-lists/ht09_contact_list.txt     |  |V| = 5.351   | |E| = 20.817     2.727 min
# /edge-lists/twitter.txt               |  |V| = 4.605   | |E| = 23.736     352.0 min
# /edge-lists/fb-messages.txt           |  |V| = 1.899   | |E| = 61.734
# /edge-lists/email-dnc.txt             |  |V| = 1.891   | |E| = 39.264     67.23 min
# /edge-lists/tij_SFHH.txt              |  |V| = 403     | |E| = 70.261
# /edge-lists/fb-forum.txt              |  |V| = 899     | |E| = 33.720
# reptilia-tortoise-network-fi.txt      |  |V| = 787     | |E| = 1.713      0.053 min
# /edge-lists/aves-weaver-social.txt    |  |V| = 445     | |E| = 1.426      0.022 min
# /edge-lists/example_graph1.txt        |  |V| = 7       | |E| = 18         0.005 min
# /edge-lists/example_graph2.txt        |  |V| = 7       | |E| = 9          0.005 min
