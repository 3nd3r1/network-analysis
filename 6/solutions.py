import matplotlib.pyplot as plt
import networkx as nx


n = 500
m_values = [1, 5, 9]

plt.figure(figsize=(16, 6), dpi=300)

for i, m in enumerate(m_values):
    graph = nx.barabasi_albert_graph(n, m)

    degree_counts = {}

    for _, degree in graph.degree():  # type: ignore
        if degree not in degree_counts:
            degree_counts[degree] = 0
        degree_counts[degree] += 1

    plt.subplot(1, 3, i + 1)
    plt.loglog(degree_counts.keys(), degree_counts.values(), "o")
    plt.xlabel("Degree", fontsize=18)
    plt.ylabel("Number of nodes", fontsize=18)
    plt.title(f"Barabasi-Albert Graph (n={n}, m={m})", fontsize=18)
    plt.grid(True, which="both")

plt.suptitle(
    "Figure 1: Degree Distribution of Barabasi-Albert Graphs With Different m",
    fontsize=20,
)
plt.tight_layout()

caption = """The plots show the degree distribution of Barabasi-Albert graphs with 500 nodes for three values of m (1, 5, 9).\n The x-axis shows the degree and the y-axis shows the count of nodes with that degree in log-log scale.\n All graphs show the expected power-law shape. Higher m moves the distribution more to the higher degrees, but still keeping the slope."""

plt.figtext(0.5, -0.1, caption, ha="center", fontsize=14, wrap=True)

plt.savefig("figure-1.png", dpi=300, bbox_inches="tight")
