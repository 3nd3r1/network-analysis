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

    # If there is a - edge within a group return NO
    for edge in graph.edges(data=True):
        if (
            node_component[edge[0]] == node_component[edge[1]]
            and edge[2]["sign"] == "-"
        ):
            return False

    # Replace each group with one super node
    graph_supernodes = nx.Graph()
    graph_supernodes.add_nodes_from(range(num_components))
    for node, i in node_component.items():
        for edge in graph.edges(node):
            if node_component[edge[1]] != i and not graph_supernodes.has_edge(
                i, node_component[edge[1]]
            ):
                graph_supernodes.add_edge(i, node_component[edge[1]])

    # Perform BFS from some node if two nodes in the same layer are connected then return NO
    for node in graph_supernodes.nodes():
        for layer in nx.bfs_layers(graph_supernodes, node):
            for i in range(0, len(layer)):
                for j in range(i + 1, len(layer)):
                    if graph_supernodes.has_edge(layer[i], layer[j]):
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
