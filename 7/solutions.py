import random

import networkx as nx


def to_directed(graph: nx.Graph) -> nx.DiGraph:
    digraph = nx.DiGraph()
    digraph.add_nodes_from(graph.nodes())

    for edge in graph.edges():
        if edge[0] < edge[1]:
            digraph.add_edge(edge[0], edge[1])
        else:
            digraph.add_edge(edge[1], edge[0])

    return digraph


graphs = {
    "bull_graph": to_directed(nx.bull_graph()),
    "krackhardt_kite_graph": to_directed(nx.krackhardt_kite_graph()),
    "petersen_graph": to_directed(nx.petersen_graph()),
}

for graph_name, graph in graphs.items():
    print(f"{graph_name} (n={graph.number_of_nodes()}, m={graph.number_of_edges()})")

    node_list = list(graph.nodes())
    edge_list = list(graph.edges())

    a_2 = random.sample(node_list, 3)
    a_1 = random.sample(a_2, 2)
    u_node = random.choice([node for node in node_list if node not in a_2])

    sets = {
        "A_1": a_1,
        "A_2": a_2,
        "A_1 + u": a_1 + [u_node],
        "A_2 + u": a_2 + [u_node],
    }
    set_results = {k: 0 for k in sets.keys()}

    x_amount = 1 << len(edge_list)
    for i in range(x_amount):
        x = [edge_list[j] for j in range(len(edge_list)) if (i >> j) & 1]

        sir_graph = nx.DiGraph()
        sir_graph.add_nodes_from(node_list)
        sir_graph.add_edges_from(x)

        for name, nodes in sets.items():
            visited = set()
            for node in nodes:
                for v in nx.bfs_tree(sir_graph, node).nodes():
                    if v not in visited:
                        visited.add(v)
                        set_results[name] += 1

    s_a_1 = set_results["A_1"] / x_amount
    s_a_2 = set_results["A_2"] / x_amount
    s_a_1_u = set_results["A_1 + u"] / x_amount
    s_a_2_u = set_results["A_2 + u"] / x_amount

    print(f"s(A_1) <= s(A_2) {'-' * 10}> {s_a_1} <= {s_a_2}")
    print(
        f"s(A_1 + {{u}}) - S(A_1) >= s(A_2 + {{u}}) - s(A_2) {'-' * 10}> {s_a_1_u - s_a_1} >= {s_a_2_u - s_a_2}"
    )
