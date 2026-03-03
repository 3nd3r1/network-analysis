import ast
import csv

import matplotlib.pyplot as plt
import networkx as nx
from networkx.algorithms.community import louvain_communities


def print_structure(graph):
    print(f"The network: {graph}")
    print(f"The network is connected: {nx.is_connected(graph)}")
    print(
        f"The network has {nx.number_connected_components(graph)} connected components"
    )
    print(
        f"The size of the largest connected component is: {len(max(nx.connected_components(graph), key=len))}"
    )
    print(f"Network density: {nx.density(graph)}")
    degrees = [d[1] for d in nx.degree(graph)]
    print(f"Min degree: {min(degrees)}")
    print(f"Max degree: {max(degrees)}")
    print(f"Avg degree: {sum(degrees) / len(degrees)}")


def create_degree_histogram(grapha, graphb):
    main_degrees = [d[1] for d in nx.degree(grapha)]
    rev_degrees = [d[1] for d in nx.degree(graphb)]

    plt.subplots(1, 2, figsize=(16, 8))
    plt.suptitle("Figure 1: Degree Distribution", fontsize=22)

    plt.subplot(1, 2, 1)
    plt.hist(main_degrees, bins=50)
    plt.xlabel("Degree", fontsize=18)
    plt.ylabel("Number of nodes", fontsize=18)
    plt.yscale("log")
    plt.title("Main Network", fontsize=20)
    plt.tick_params(labelsize=14)

    plt.subplot(1, 2, 2)
    plt.hist(rev_degrees, bins=20)
    plt.xlabel("Degree", fontsize=18)
    plt.ylabel("Number of nodes", fontsize=18)
    plt.yscale("log")
    plt.title("Reviewer Sub-network", fontsize=20)
    plt.tick_params(labelsize=14)

    caption = "Figure 1 shows the degree distributions for the main network and the reviewer sub-network.\nIn both networks most nodes have only a few connections while a small number of nodes have more than average connections."
    plt.figtext(0.5, 0.045, caption, ha="center", fontsize=14, wrap=True)
    plt.tight_layout(rect=[0, 0.10, 1, 1])  # type: ignore
    plt.savefig("./figures/figure-1.png", dpi=300)


def print_top_centrality_nodes(graph, allowed_nodes):
    top = {}

    top["Degree Centrality"] = sorted(
        [n for n in nx.degree_centrality(graph).items() if n[0] in allowed_nodes],
        key=lambda x: x[1],
        reverse=True,
    )[:5]
    top["Betweenness Centrality"] = sorted(
        [
            n
            for n in nx.betweenness_centrality(
                graph, k=min(250, graph.number_of_nodes())
            ).items()
            if n[0] in allowed_nodes
        ],
        key=lambda x: x[1],
        reverse=True,
    )[:5]
    top["Closeness Centrality"] = sorted(
        [n for n in nx.closeness_centrality(graph).items() if n[0] in allowed_nodes],
        key=lambda x: x[1],
        reverse=True,
    )[:5]
    top["Pagerank Centrality"] = sorted(
        [n for n in nx.pagerank(graph).items() if n[0] in allowed_nodes],
        key=lambda x: x[1],
        reverse=True,
    )[:5]

    print("| Rank | " + " | ".join(m for m in top.keys()) + " |")
    print("|------|" + "|".join("---" for _ in top.keys()) + "|")
    for i in range(5):
        row = f"| {i + 1} |"
        for m in top.keys():
            name, val = top[m][i]
            row += f" {name} : {val:.4f} |"
        print(row)


def create_community_bar(communities):
    community_sizes = sorted([len(com) for com in communities], reverse=True)

    plt.subplots(figsize=(10, 6))
    plt.bar(range(len(community_sizes)), community_sizes)
    plt.xlabel("Community", fontsize=18)
    plt.ylabel("Number of nodes", fontsize=18)
    plt.title("Figure 2: Community Sizes Using Louvain", fontsize=20)
    plt.tick_params(labelsize=14)

    caption = "Figure 2 shows the sizes of the 49 communities detected by Louvain.\nThe community sizes decrease linearly with no big gaps.\nThis means that the network does not have strongly separated clusters."
    plt.figtext(
        0.5,
        -0.1,
        caption,
        ha="center",
        fontsize=14,
    )

    plt.savefig("figures/figure-2.png", dpi=300, bbox_inches="tight")


def print_commnity_strength(graph, communities):
    node_to_community = {}
    for i, community in enumerate(communities):
        for node in community:
            node_to_community[node] = i

    inside_strength = [
        sum(d[1] for d in data["co_authorship"])
        for a, b, data in graph.edges(data=True)
        if node_to_community[a] == node_to_community[b]
    ]
    outside_strength = [
        sum(d[1] for d in data["co_authorship"])
        for a, b, data in graph.edges(data=True)
        if node_to_community[a] != node_to_community[b]
    ]

    print(
        f"Avg edge strength inside community: {sum(inside_strength) / len(inside_strength)}"
    )
    print(
        f"Avg edge strength outside community: {sum(outside_strength) / len(outside_strength)}"
    )


def do_q1():
    global graph, reviewers_graph
    print("Main graph:")
    print_structure(graph)
    print()
    print("Reviewer subgraph:")
    print_structure(reviewers_graph)

    create_degree_histogram(graph, reviewers_graph)


def do_q2():
    global graph, reviewers
    print("Top centrality of reviewers:")
    print_top_centrality_nodes(graph, reviewers)
    print()
    print("Top centrality of non-reviewers:")
    print_top_centrality_nodes(graph, [n for n in graph.nodes() if n not in reviewers])


def do_q3():
    global graph
    communities = louvain_communities(graph, seed=123)
    print(f"Number of communities: {len(communities)}")

    create_community_bar(communities)
    print_commnity_strength(graph, communities)


graph = nx.Graph()
reviewers_graph = None
reviewers = set()

with open("./data/coauthorship-conflicts-sigmod24.csv") as fp:
    reader = csv.reader(fp)
    next(reader)
    for row in reader:
        author, reviewer, reviewer_dblp, co_authorship, _ = row
        reviewers.add(reviewer)
        co_authorship = ast.literal_eval(co_authorship)
        graph.add_edge(
            author, reviewer, reviewer_dblp=reviewer_dblp, co_authorship=co_authorship
        )
    reviewers_graph = graph.subgraph(reviewers)

    do_q1()
    do_q2()
    do_q3()
