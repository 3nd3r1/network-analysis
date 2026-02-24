import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
from scipy.sparse.linalg import eigsh


def do_part_1(X, Y, u2, u3):
    colors = ["red", "blue", "green", "yellow"]
    caption_generic = "Scatter plot of node attributes (X) and spectral embedding (u2,u3). Points colored by node label (Y)."
    captions = {
        1: f"{caption_generic}\nThe node attributes separate the nodes into 4 groups but all node labels overlap.\nThe spectral embedding also fails to separate labels with most nodes clustered.",
        2: f"{caption_generic}\nThe node attributes almost separate the labels. Label 0 and 2 are grouped to the left and labels 1 and 3 on the right.\n But the two labels overlap inside the groups.\nThe spectral embedding does nothing with most nodes clustered very closely.",
        3: f"{caption_generic}\nThe node attributes separate the labels perfectly into 4 groups.\nThe spectral embedding does not, everything is still clustered.",
    }
    plt.subplots(1, 2, figsize=(16, 7))
    plt.suptitle(f"Figure 1{chr(ord('a') + i)}: Network {i}", fontsize=20)

    plt.subplot(1, 2, 1)
    plt.scatter(x=[x[0] for x in X], y=[x[1] for x in X], c=[colors[y] for y in Y])
    plt.xlabel("X1", fontsize=18)
    plt.ylabel("X2", fontsize=18)
    plt.title("Node Attributes (X)", fontsize=18)
    plt.legend(
        handles=[mpatches.Patch(color=colors[c], label=f"Y = {c}") for c in range(4)],
        fontsize=14,
    )

    plt.subplot(1, 2, 2)
    plt.scatter(x=u2, y=u3, c=[colors[y] for y in Y])
    plt.xlabel("u2", fontsize=18)
    plt.ylabel("u3", fontsize=18)
    plt.title("Spectral Embedding (u2, u3)", fontsize=18)
    plt.legend(
        handles=[mpatches.Patch(color=colors[c], label=f"Y = {c}") for c in range(4)],
        fontsize=14,
    )

    plt.figtext(0.5, -0.1, captions[i], ha="center", fontsize=14, wrap=True)

    plt.tight_layout()
    plt.savefig(f"figure-1{chr(ord('a') + i)}.png", dpi=300, bbox_inches="tight")
    plt.close()


def do_part_2(A):
    graph = nx.from_numpy_matrix(A)
    print(graph)


for i in range(1, 4):
    A = np.load(f"./data/network_{i}_A.pkl", allow_pickle=True).astype("float")
    A = A - np.eye(A.shape[0])
    X = np.load(f"./data/network_{i}_X.pkl", allow_pickle=True).astype("float")
    Y = np.load(f"./data/network_{i}_Y.pkl", allow_pickle=True).astype(int)
    D = np.diag(A.sum(axis=1))
    L = D - A
    w, u = eigsh(L, k=3)
    u2, u3 = u.T[1], u.T[2]  # Laplacian eigenvector u2, u3
    w2, w3 = w[1], w[2]  # Laplacian eigenvalues w2, w3

    do_part_1(X, Y, u2, u3)
    do_part_2(A)
