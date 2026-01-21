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
    {
        "title": "Barabasi-Albert Network (n=100, m=5)",
        "graph": G1,
        "measure_caption": "We see a strong correlation, indicating that high degree nodes have high PageRank.",
        "network_caption": "The network has a few large red nodes in the center. These nodes have high degree and high PageRank, confirming the correlation in Figure 1a.",
    },
    {
        "title": "Watts-Strogatz Network (n=100, k=6, p=0.3)",
        "graph": G2,
        "measure_caption": "The horizontal bands appear because most nodes have the same degree, but their PageRank differs based on their neighbors.",
        "network_caption": "There is not as much degree variance, but the PageRank varies more with red nodes scattered across the network. This shows that PageRank doesn't only depend on degree.",
    },
    {
        "title": "Erdos-Renyi Network (n=200, p=0.05)",
        "graph": G3,
        "measure_caption": "We see a strong correlation since random edges make all links roughly equal in value.",
        "network_caption": "Large red nodes are in the center while small blue nodes are on the edges. PageRank and degree match, confirming that degree and PageRank are correlated in random graphs.",
    },
    {
        "title": "P2P Gnutella04 Network",
        "graph": G4,
        "measure_caption": "There is a correlation but with more scatter than the synthetic graphs.",
        "network_caption": "A BFS subgraph of 1000 nodes from the largest connected component. Most nodes are small and blue with a few orange nodes scattered in the center. The network has many leaf nodes with low degree and low PageRank.",
    },
    {
        "title": "P2P Gnutella09 Network",
        "graph": G5,
        "measure_caption": "Similar to Gnutella04 with a clear correlation.",
        "network_caption": "Similar structure to Gnutella04. Orange nodes appear in the center surrounded by many blue nodes.",
    },
    {
        "title": "Web Google Network",
        "graph": G6,
        "measure_caption": "The spread is wider here because in web graphs getting links from important pages matters more than just having many links.",
        "network_caption": "A BFS subgraph of 1000 nodes. The one red node in the center is the most important page. Most of the network is blue, showing that only a small number of pages are really important in web graphs.",
    },
]


# measure plots
if generate_measure_plots:
    for i, graph_info in enumerate(graph_infos):
        graph = graph_info["graph"]
        title = graph_info["title"]
        caption = (
            "The plot shows PageRank (x) against normalized degree centrality (y) for each node. "
            + graph_info["measure_caption"]
        )

        pr_score = list(nx.pagerank(graph).values())

        if graph.is_directed():
            degc = list(nx.in_degree_centrality(graph).values())
        else:
            degc = list(nx.degree_centrality(graph).values())

        plt.figure(figsize=(10, 8), dpi=300)
        plt.scatter(pr_score, degc)
        plt.xlabel("PageRank", fontsize=18)
        plt.ylabel("Normalized Degree Centrality", fontsize=18)
        plt.ticklabel_format(axis="y", style="sci", scilimits=(0, 0))
        plt.ticklabel_format(axis="x", style="sci", scilimits=(0, 0))
        plt.title(
            f"Figure 1{chr(ord('a') + i)}: PageRank vs Normalized Degree Centrality\n{title}",
            fontsize=18,
        )

        plt.figtext(0.5, 0, caption, ha="center", wrap=True, fontsize=12)

        plt.savefig(f"figure-1{chr(ord('a') + i)}.png", dpi=300, bbox_inches="tight")

# network plots
if generate_network_plots:
    for i, graph_info in enumerate(graph_infos):
        graph = graph_info["graph"]
        title = graph_info["title"]
        subtitle = ""
        caption = graph_info["network_caption"]

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

        plt.figure(figsize=(10, 8), dpi=300)
        plt.title(
            f"Figure 2{chr(ord('a') + i)}: Network Visualization with PageRank and Degree\n{title} {subtitle}\nColor = PageRank | Size = Degree"
        , fontsize=18)
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
        plt.figtext(0.5, 0, caption, ha="center", wrap=True, fontsize=12)

        plt.savefig(f"figure-2{chr(ord('a') + i)}.png", dpi=300, bbox_inches="tight")
