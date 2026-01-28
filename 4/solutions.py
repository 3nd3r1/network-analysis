import matplotlib.pyplot as plt
import networkx as nx


def draw_supernodes_graph(graph: nx.Graph, node_component: dict) -> None:
    pos = nx.bfs_layout(graph, 0)
    nx.draw(graph, pos)
    node_labels = {
        n: f"{n}\n{str([node for node, supernode in node_component.items() if supernode == n])}"
        for n in graph.nodes()
    }
    nx.draw_networkx_labels(graph, pos, labels=node_labels)
    edge_labels = {
        (u, v): f"{d['node_a']} to {d['node_b']}" for u, v, d in graph.edges(data=True)
    }
    nx.draw_networkx_edge_labels(graph, pos, edge_labels=edge_labels)
    plt.show()


def build_the_odd_cycle(
    graph_supernodes: nx.Graph,
    node_i: int,
    node_j: int,
    graph: nx.Graph,
) -> list[int]:
    """
    Basically we get the BFS paths from the 0 supernode to the two
    supernodes that have an edge in the same layer.
    Then we get the actual nodes from the original graph and build the cycle.
    """
    supernode_bfs_tree = nx.bfs_tree(graph_supernodes, 0)

    path_i = nx.shortest_path(supernode_bfs_tree, 0, node_i)
    path_j = nx.shortest_path(supernode_bfs_tree, 0, node_j)
    actual_path_i = []
    actual_path_j = []

    for k in range(1, len(path_i)):
        actual_path_i.append(graph_supernodes[path_i[k - 1]][path_i[k]]["node_a"])
        actual_path_i.append(graph_supernodes[path_i[k - 1]][path_i[k]]["node_b"])
    for k in range(1, len(path_j)):
        actual_path_j.append(graph_supernodes[path_j[k - 1]][path_j[k]]["node_a"])
        actual_path_j.append(graph_supernodes[path_j[k - 1]][path_j[k]]["node_b"])

    actual_path = actual_path_i + list(reversed(actual_path_j))
    final_path = [actual_path[0]]
    for k in range(1, len(actual_path)):
        if actual_path[k] == final_path[-1]:
            continue
        elif not graph.has_edge(final_path[-1], actual_path[k]):
            final_path.extend(
                nx.shortest_path(graph, final_path[-1], actual_path[k])[1:]
            )
        else:
            final_path.append(actual_path[k])

    final_path.append(final_path[0])
    return final_path


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

    # If there is a - edge within a group return NO
    for edge in graph.edges(data=True):
        if (
            node_component[edge[0]] == node_component[edge[1]]
            and edge[2]["sign"] == "-"
        ):
            cycle = nx.shortest_path(graph_plus, edge[0], edge[1]) + [edge[0]]
            print(f"The odd cycle is {cycle}")
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
                    cycle = build_the_odd_cycle(
                        graph_supernodes, layer[i], layer[j], graph
                    )
                    print(f"The odd cycle is {cycle}")
                    return False

    # Return YES
    print(f"The disjoint sets are: {disjoint_set_a} and {disjoint_set_b}")
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

print("Graph N1:")
if balance_test(graph_n1):
    print("The graph is balanced")
else:
    print("The graph is not balanced")
print()

print("Graph N2:")
if balance_test(graph_n2):
    print("The graph is balanced")
else:
    print("The graph is not balanced")
