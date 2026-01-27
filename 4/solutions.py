import matplotlib.pyplot as plt
import networkx as nx


def balance_test(graph: nx.Graph) -> bool:
    graph_plus = nx.Graph()
    for node in graph.nodes():
        graph_plus.add_node(node)
    for edge in graph.edges(data=True):
        if edge[2]["sign"] == "+":
            graph_plus.add_edge(edge[0], edge[1])

    # Group nodes by connected component
    node_component = {}
    num_components = 0
    for i, component in enumerate(nx.connected_components(graph_plus)):
        num_components += 1
        for node in component:
            node_component[node] = i
    print(node_component)

    # If there is a - edge within a group return NO
    for edge in graph.edges(data=True):
        if (
            node_component[edge[0]] == node_component[edge[1]]
            and edge[2]["sign"] == "-"
        ):
            cycle = nx.shortest_path(graph_plus, edge[0], edge[1]) + [edge[0]]
            print(f"The graph is not balanced and the odd cycle is {cycle}")
            return False

    # Replace each group with one super node
    graph_supernodes = nx.Graph()
    graph_supernodes.add_nodes_from(range(num_components))
    for node, i in node_component.items():
        for edge in graph.edges(node):
            if node_component[edge[1]] != i and not graph_supernodes.has_edge(
                i, node_component[edge[1]]
            ):
                graph_supernodes.add_edge(
                    i, node_component[edge[1]], node_a=node, node_b=edge[1]
                )

    # Perform BFS from some node if two nodes in the same layer are connected then return NO
    # We start the bfs from node 0. We assume that the supernodes are all connected.
    disjoint_set_a = set()
    disjoint_set_b = set()
    tree = nx.bfs_tree(graph_supernodes, 0)

    for i, layer in enumerate(nx.bfs_layers(graph_supernodes, 0)):
        for supernode in layer:
            for node in graph:
                if node_component[node] == supernode:
                    if i % 2 == 0:
                        disjoint_set_a.add(node)
                    else:
                        disjoint_set_b.add(node)

        for i in range(0, len(layer)):
            for j in range(i + 1, len(layer)):
                if graph_supernodes.has_edge(layer[i], layer[j]):
                    pos = nx.bfs_layout(graph_supernodes, 0)
                    nx.draw(graph_supernodes, pos, with_labels=True)
                    plt.show()
                    path_left = nx.shortest_path(tree, 0, layer[i])
                    path_right = nx.shortest_path(tree, 0, layer[j])
                    print(path_left)
                    print(path_right)
                    actual_path_left = []
                    actual_path_right = []
                    for i in range(1, len(path_left) - 1):
                        node_left = graph_supernodes[path_left[i - 1]][path_left[i]][
                            "node_b"
                        ]
                        node_right = graph_supernodes[path_left[i]][path_left[i + 1]][
                            "node_a"
                        ]
                        actual_path_left.extend(
                            nx.shortest_path(graph, node_left, node_right)
                        )
                    for i in range(1, len(path_right) - 1):
                        node_left = graph_supernodes[path_right[i - 1]][path_right[i]][
                            "node_b"
                        ]
                        node_right = graph_supernodes[path_right[i]][path_right[i + 1]][
                            "node_a"
                        ]
                        actual_path_right.extend(
                            nx.shortest_path(graph, node_left, node_right)
                        )
                    print(actual_path_left)
                    print(actual_path_right)

                    return False

    # Return YES
    return True


graph_n1 = nx.read_edgelist(
    "graph_n1.edgelist",
    nodetype=int,
    data=[("sign", str)],  # type: ignore
)
graph_n2 = nx.read_edgelist(
    "graph_n2.edgelist",
    nodetype=int,
    data=[("sign", str)],  # type: ignore
)

print(balance_test(graph_n1))
print(balance_test(graph_n2))
