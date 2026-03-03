import ast
import csv

import matplotlib.pyplot as plt
import networkx as nx


def print_structure(graph):
    print(f"The network: {graph}")
    print(f"The network is connected: {nx.is_connected(graph)}")
    print(
        f"The network has {nx.number_connected_components(graph)} connected components"
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


def do_q1():
    global graph, reviewers_graph
    print("Main graph:")
    print_structure(graph)
    print()
    print("Reviewer subgraph:")
    print_structure(reviewers_graph)

    create_degree_histogram(graph, reviewers_graph)


def do_q2():
    global graph, reviewers_graph
    print(nx.degree_centrality(graph))


graph = nx.Graph()
reviewers_graph = None

with open("./data/coauthorship-conflicts-sigmod24.csv") as fp:
    reader = csv.reader(fp)
    next(reader)
    reviewers = set()
    for row in reader:
        author, reviewer, reviewer_dblp, co_authorship, _ = row
        reviewers.add(reviewer)
        co_authorship = ast.literal_eval(co_authorship)
        graph.add_edge(
            author, reviewer, reviewer_dblp=reviewer_dblp, co_authorship=co_authorship
        )
    reviewers_graph = graph.subgraph(reviewers)

    do_q1()
