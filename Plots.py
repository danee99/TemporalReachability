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

# DATASETS:
# /edge-lists/wiki_talk_nl.txt          |  |V| = 225.749 | |E| = 1.554.698
# /edge-lists/wikipediasg.txt           |  |V| = 208.142 | |E| = 810.702
# /edge-lists/facebook.txt              |  |V| = 63.731  | |E| = 817.035
# /edge-lists/infectious.txt            |  |V| = 10.972  | |E| = 415.912    234.74493443965912 minutes
# /edge-lists/ht09_contact_list.txt     |  |V| = 5.351   | |E| = 20.817     2.914724922180176 minutes
# /edge-lists/tij_SFHH.txt              |  |V| = 3.906   | |E| = 70.261     2.8707066059112547 minutes
# /edge-lists/twitter.txt               |  |V| = 4.605   | |E| = 23.736     402.64135769208275 minutes
# /edge-lists/email-dnc.txt             |  |V| = 1.891   | |E| = 39.264     67.2289342880249 minutes
# /edge-lists/aves-weaver-social.txt    |  |V| = 445     | |E| = 1.426      0.021833324432373048 minutes
