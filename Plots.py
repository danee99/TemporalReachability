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
