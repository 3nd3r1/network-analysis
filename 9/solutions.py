from typing import List, Tuple

import matplotlib.pyplot as plt
import networkx as nx


def get_edges_with_highest_betweennes(graph: nx.Graph) -> List[Tuple[int, int]]:
    betweennes_dict = {}
    max_betweennes = 0
    for i in range(0, graph.number_of_nodes()):
        for j in range(i + 1, graph.number_of_nodes()):
            node_a = list(graph.nodes())[i]
            node_b = list(graph.nodes())[j]
            try:
                paths = list(nx.all_shortest_paths(graph, node_a, node_b))
            except nx.NetworkXNoPath:
                continue
            for path in paths:
                for edge in zip(path, path[1:]):
                    edge = tuple(sorted(edge))
                    if edge not in betweennes_dict:
                        betweennes_dict[edge] = 0
                    betweennes_dict[edge] += 1 / len(paths)
                    max_betweennes = max(max_betweennes, betweennes_dict[edge])
    ans = []
    for edge, betweennes in betweennes_dict.items():
        if betweennes >= max_betweennes:
            ans.append(edge)
    return ans


graph = nx.read_edgelist("graph.edgelist", nodetype=str)
pos = nx.spring_layout(graph)

for i in range(1, 6):
    edges_to_remove = get_edges_with_highest_betweennes(graph)
    graph.remove_edges_from(edges_to_remove)

    partitions = list(nx.connected_components(graph))

    removed_str = ", ".join([f"({a}, {b})" for a, b in edges_to_remove])
    partition_str = str(partitions)

    print(f"Step {i}: {partition_str}")

    plt.figure(figsize=(10, 8), dpi=300)
    nx.draw(graph, with_labels=True, pos=pos, font_size=18, node_size=800)
    plt.title(f"Girvan-Newman: Step {i}", fontsize=20)
    plt.figtext(
        0.5,
        -0.05,
        f"Removed edges: {removed_str}\nPartitions: {partition_str}",
        ha="center",
        fontsize=14,
        wrap=True,
    )
    plt.savefig(f"figure-{i}.png", dpi=300, bbox_inches="tight")
