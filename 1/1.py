import matplotlib.pyplot as plt
import networkx as nx


G = nx.read_weighted_edgelist("./course_network_l2.adjlist")
print(f"Biggest degree {G.degree(max(G, key=G.degree))}")

average_degree = sum(x[1] for x in G.degree()) / G.number_of_nodes()
print(f"Average degree {average_degree}")

plt.figure(figsize=(12, 10))
pos_spring = nx.spring_layout(G)

top5_nodes = {node for node in sorted(G, key=G.degree, reverse=True)[:5]}
big_nodes = {node[0] for node in G.degree() if node[1] > average_degree}
other_nodes = set(G) - big_nodes

min_weight = min(nx.get_edge_attributes(G, "weight").values())
max_weight = max(nx.get_edge_attributes(G, "weight").values())

nx.draw_networkx_nodes(
    G, pos=pos_spring, nodelist=big_nodes, node_size=800, node_color="green"
)
nx.draw_networkx_nodes(
    G, pos=pos_spring, nodelist=other_nodes, node_size=200, node_color="purple"
)


for edge, weight in nx.get_edge_attributes(G, "weight").items():
    width_normalized = 0.5 + 4 * (weight - min_weight) / (max_weight - min_weight)
    nx.draw_networkx_edges(
        G,
        pos=pos_spring,
        edgelist=[edge],
        width=width_normalized,
        edge_color="blue",
        alpha=0.6,
    )

nx.draw_networkx_labels(
    G,
    pos=pos_spring,
    labels={n: n for n in top5_nodes},
    font_size=10,
    font_weight="bold",
)

plt.savefig("1-2.png")
plt.show()
