import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
from scipy.sparse.linalg import eigsh
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split


colors = ["red", "blue", "green", "yellow"]


def do_part_1(i, X, Y, u2, u3):
    caption_generic = "Scatter plot of node attributes (X) and spectral embedding (u2,u3). Points colored by node label (Y)."
    captions = {
        1: f"{caption_generic}\nThe node attributes separate the nodes into 4 groups but all node labels overlap.\nThe spectral embedding also fails to separate labels with most nodes clustered.",
        2: f"{caption_generic}\nThe node attributes almost separate the labels. Label 0 and 2 are grouped to the left and labels 1 and 3 on the right.\n But the two labels overlap inside the groups.\nThe spectral embedding does nothing with most nodes clustered very closely.",
        3: f"{caption_generic}\nThe node attributes separate the labels perfectly into 4 groups.\nThe spectral embedding does not, everything is still clustered.",
    }
    plt.subplots(1, 2, figsize=(16, 7))
    plt.suptitle(f"Figure 1{chr(ord('a') + i - 1)}: Network {i}", fontsize=20)

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
    plt.savefig(f"figure-1{chr(ord('a') + i - 1)}.png", dpi=300, bbox_inches="tight")
    plt.close()


def do_part_2(i, A, Y):
    captions = {
        1: "Network 1 visualized using spectral and spring layouts.\n The spectral layout  separates nodes into 4 distinct groups and the node colors show these match the node label (Y).\n The spring layout does not separate nodes, but we can see that the node labels are clearly separate.",
        2: "Network 2 visualized using spectral and spring layouts.\n The spectral layout separates nodes into 4 groups, but labels {0,1} and {2,3} overlap in the bottom-left and upper-right corners respectively.\n The spring layout does not separate nodes, but we can see a left-right split between labels {2,3} and {0,1}.",
        3: "Network 3 visualized using spectral and spring layouts.\n The spectral layout separates nodes into 4 regions, but the node labels are completely mixed.\n The spring layout does not separate nodes and shows no clear node label grouping.",
    }

    graph = nx.from_numpy_array(A)
    pos_spectral = nx.spectral_layout(graph)
    pos_spring = nx.spring_layout(graph, seed=123)

    plt.subplots(1, 2, figsize=(20, 9))
    plt.suptitle(f"Figure 2{chr(ord('a') + i - 1)}: Network {i}", fontsize=24)

    plt.subplot(1, 2, 1)
    nx.draw(
        graph,
        pos=pos_spectral,
        node_size=50,
        width=0.1,
        edge_color="gray",
        node_color=[colors[y] for y in Y],
    )
    plt.legend(
        handles=[mpatches.Patch(color=colors[c], label=f"Y = {c}") for c in range(4)],
        fontsize=14,
    )
    plt.title("Spectral Layout", fontsize=20)

    plt.subplot(1, 2, 2)
    nx.draw(
        graph,
        pos=pos_spring,
        node_size=50,
        width=0.1,
        edge_color="gray",
        node_color=[colors[y] for y in Y],
    )
    plt.title("Spring Layout", fontsize=20)
    plt.legend(
        handles=[mpatches.Patch(color=colors[c], label=f"Y = {c}") for c in range(4)],
        fontsize=14,
    )

    plt.figtext(0.5, -0.02, captions[i], ha="center", fontsize=18, wrap=True)
    plt.tight_layout()
    plt.savefig(f"figure-2{chr(ord('a') + i - 1)}.png", dpi=300, bbox_inches="tight")
    plt.close()


def do_part_3(i, X, Y, u2, u3):
    captions = {
        1: "All feature sets perform poorly (less than 0.40 accuracy).\n The spectral embedding (u2, u3) slightly outperforms X alone, but no feature set is effective for label prediction.",
        2: "(X, u2, u3) achieves the best accuracy (0.58) outperforming X and [u2,u3] alone.\n This shows that node attributes and network structure combined are able to accurately predict Y.",
        3: "X alone achieves perfect accuracy and adding U does not improve it.\n Spectral embedding alone is very unaccurate, confirming that network structure alone is not enough.",
    }
    features_list = [
        u2.reshape(-1, 1),
        u3.reshape(-1, 1),
        np.column_stack([u2, u3]),
        X,
        np.hstack([X, np.column_stack([u2, u3])]),
    ]

    labels = ["[u2]", "[u3]", "[u2, u3]", "X", "[X, u2, u3]"]
    accuracies = []

    for features in features_list:
        x_train, x_test, y_train, y_test = train_test_split(
            features, Y, test_size=0.2, random_state=123
        )
        model = RandomForestClassifier(random_state=123)
        model.fit(x_train, y_train)
        y_prediction = model.predict(x_test)
        accuracies.append(accuracy_score(y_test, y_prediction))

    plt.figure(figsize=(12, 7))

    plt.bar(labels, accuracies)
    plt.ylabel("Accuracy", fontsize=18)
    plt.xlabel("Features", fontsize=18)
    plt.title(
        f"Figure 3{chr(ord('a') + i - 1)}: Random Forest Accuracy with Network {i}",
        fontsize=18,
    )
    plt.ylim(0, 1)
    plt.xticks(fontsize=14)
    plt.yticks(fontsize=14)

    plt.figtext(0.5, 0.05, captions[i], ha="center", fontsize=14, wrap=True)
    plt.tight_layout(rect=[0, 0.10, 1, 1]) # type: ignore
    plt.savefig(f"figure-3{chr(ord('a') + i - 1)}.png", dpi=300)
    plt.close()


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

    # do_part_1(i, X, Y, u2, u3)
    # do_part_2(i, A, Y)
    do_part_3(i, X, Y, u2, u3)
