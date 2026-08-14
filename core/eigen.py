import numpy as np

REAL_TOL = 1e-9


def compute_eigen(M):
    """Retorna (eigenvalues brutos, lista de (autovalor real, autovetor unitário real))
    só com os pares cujo autovalor não tem parte imaginária relevante — uma matriz de
    rotação pura, por exemplo, não tem direção invariante real nenhuma."""
    eigenvalues, eigenvectors = np.linalg.eig(M)
    real_pairs = []
    for i in range(len(eigenvalues)):
        val = eigenvalues[i]
        if abs(val.imag) < REAL_TOL:
            vec = eigenvectors[:, i].real
            norm = np.linalg.norm(vec)
            if norm > REAL_TOL:
                real_pairs.append((val.real, vec / norm))
    return eigenvalues, real_pairs


def determinant(M):
    return float(np.linalg.det(M))


def trace(M):
    return float(np.trace(M))
