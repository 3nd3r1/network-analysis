import numpy as np
from scipy.sparse.linalg import eigsh


for i in range(1, 4):
    A = np.load(f"./data/network_{i}_A.pkl", allow_pickle=True).astype("float")
    A = A - np.eye(A.shape[0])
    X = np.load(f"./data/network_{i}_X.pkl", allow_pickle=True).astype("float")
    Y = np.load(f"./data/network_{i}_Y.pkl", allow_pickle=True).astype(int)
    D = np.diag(A.sum(axis=1))
    L = D - A
    w, v = eigsh(L, k=3)
    u2, u3 = v[1], v[2]  # Laplacian eigenvector u2, u3
    w2, w3 = w[1], w[2]  # Laplacian eigenvalues w2, w3
