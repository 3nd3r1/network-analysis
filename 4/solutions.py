import networkx as nx


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
