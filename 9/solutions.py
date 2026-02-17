from typing import List, Tuple

import matplotlib.pyplot as plt
import networkx as nx


def get_edges_with_highest_betweennes(graph: nx.Graph) -> List[Tuple[int, int]]:
    betweennes_dict = {}
    max_betweennes = 0
    for node_a in graph.nodes():
        for node_b in graph.nodes():
            if node_a == node_b:
                continue
            paths = list(nx.all_shortest_paths(graph, node_a, node_b))
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

for _ in range(5):
    nx.draw(graph, with_labels=True)
    plt.show()
    edges_to_remove = get_edges_with_highest_betweennes(graph)
    graph.remove_edges_from(edges_to_remove)
