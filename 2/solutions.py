import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import networkx as nx


generate_measure_plots = True
generate_network_plots = True

G1 = nx.barabasi_albert_graph(n=100, m=5)
G2 = nx.watts_strogatz_graph(n=100, k=6, p=0.3)
G3 = nx.erdos_renyi_graph(n=200, p=0.05)

G4 = nx.read_edgelist("data/p2p-Gnutella04.txt", create_using=nx.DiGraph())
G5 = nx.read_edgelist("data/p2p-Gnutella09.txt", create_using=nx.DiGraph())
G6 = nx.read_edgelist("data/web-Google.txt", create_using=nx.DiGraph())

graph_infos = [
    {"title": "Barabasi-Albert Network (n=100, m=5)", "graph": G1},
    {"title": "Watts-Strogatz Network (n=100, k=6, p=0.3)", "graph": G2},
    {"title": "Erdos-Renyi Network (n=200, p=0.05)", "graph": G3},
    {"title": "P2P Gnutella04 Network", "graph": G4},
    {"title": "P2P Gnutella09 Network", "graph": G5},
    {"title": "Web Google Network", "graph": G6},
]

# measure plots
if generate_measure_plots:
    for i, graph_info in enumerate(graph_infos):
        graph = graph_info["graph"]
        title = graph_info["title"]

        pr_score = list(nx.pagerank(graph).values())

        if graph.is_directed():
            degc = list(nx.in_degree_centrality(graph).values())
        else:
            degc = list(nx.degree_centrality(graph).values())

        plt.figure(figsize=(8, 6), dpi=300)
        plt.scatter(pr_score, degc)
        plt.xlabel("PageRank")
        plt.ylabel("Normalized Degree Centrality")
        plt.ticklabel_format(axis="y", style="sci", scilimits=(0, 0))
        plt.ticklabel_format(axis="x", style="sci", scilimits=(0, 0))
        plt.title(
            f"Measure Plot {i + 1}: Comparing PageRank vs Normalized Degree Centrality\n{title}"
        )
        plt.savefig(f"measureplot_{i + 1}.png")

# network plots
if generate_network_plots:
    for i, graph_info in enumerate(graph_infos):
        graph = graph_info["graph"]
        title = graph_info["title"]
        subtitle = ""

        if graph.number_of_nodes() > 1000:
            component = max(nx.weakly_connected_components(graph), key=len)
            graph = graph.subgraph(component).copy()
            subtitle = "(Largest Connected Component)"

            if graph.number_of_nodes() > 1000:
                nodes_subset = list(nx.bfs_tree(graph, list(graph.nodes())[0]).nodes())[
                    :1000
                ]
                graph = graph.subgraph(nodes_subset).copy()
                subtitle = "(BFS Subgraph of 1000 nodes)"

        pr_score = list(nx.pagerank(graph).values())
        if graph.is_directed():
            degrees = dict(graph.in_degree()).values()
        else:
            degrees = dict(graph.degree()).values()

        min_degree = min(degrees)
        max_degree = max(degrees)

        node_sizes = [
            (deg - min_degree) / (max_degree - min_degree) * 300 + 20 for deg in degrees
        ]

        plt.figure(figsize=(8, 6), dpi=300)
        plt.title(
            f"Network Plot {i + 1}: Network Visualization with PageRank and Degree\n{title} {subtitle}\nColor = PageRank | Size = Degree"
        )
        nx.draw(
            graph,
            ax=plt.gca(),
            pos=nx.spring_layout(graph),
            node_color=pr_score,
            cmap=plt.cm.coolwarm,
            node_size=node_sizes,
            edge_color="gray",
            width=0.3,
        )
        low_patch = mpatches.Patch(color="blue", label="Low")
        high_patch = mpatches.Patch(color="red", label="High")
        plt.legend(handles=[low_patch, high_patch], title="PageRank", loc="upper right")
        plt.savefig(f"networkplot_{i + 1}.png")
