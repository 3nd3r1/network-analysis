import matplotlib.pyplot as plt
import networkx as nx
import numpy as np


n = 500
p_values = [p for p in np.arange(0, 0.05, 0.001)]

f_values = []
for p in p_values:
    connected_count = 0
    graph_amount = 15
    for _ in range(graph_amount):
        graph = nx.gnp_random_graph(n, p)
        if nx.is_connected(graph):
            connected_count += 1
    f_values.append(connected_count / graph_amount)

average_sizes = []
for p in p_values:
    sizes_sum = 0
    graph_amount = 15
    for _ in range(graph_amount):
        graph = nx.gnp_random_graph(n, p)
        component = max(nx.connected_components(graph), key=len)
        sizes_sum += len(component)
    average_sizes.append(sizes_sum / graph_amount)


# Figure 1
plt.figure(figsize=(10, 8), dpi=300)
plt.scatter(p_values, f_values)
plt.xlabel("p", fontsize=18)
plt.ylabel("Empirical Relative Frequency of Connectivity", fontsize=14)
plt.title(
    f"Figure 1: Empirical Relative Frequency of Connectivity in G({n}, p)",
    fontsize=18,
)
plt.figtext(0.5, 0, f"Connectivity frequency for G({n}, p) graphs. Each point shows the frequency of connected graphs out of 15 graphs. The frequency starts increasing at around p=0.01 and they become always connected at around p=0.02", ha="center", wrap=True, fontsize=12)
plt.savefig("figure-1.png", dpi=300, bbox_inches="tight")

# Figure 2
plt.figure(figsize=(10, 8), dpi=300)
plt.scatter(p_values, average_sizes)
plt.xlabel("p", fontsize=18)
plt.ylabel("Empirical Average Size of Largest Connected Component", fontsize=14)
plt.title(
    f"Figure 2: Empirical Average Size of Largest Connected Component in G({n}, p)",
    fontsize=18,
)
plt.figtext(0.5, 0, f"Average largest component size for G({n}, p) graphs. Each point is the average of 15 graphs. The largest component starts growing rapidly at around p=0.01 and covers all 500 nodes by p=0.015.", ha="center", wrap=True, fontsize=12)
plt.savefig("figure-2.png", dpi=300, bbox_inches="tight")
