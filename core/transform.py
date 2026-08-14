import numpy as np


def apply_matrix(M, points):
    """points: array (N, 2), cada linha um ponto/vetor. Retorna M aplicado a cada um."""
    return points @ np.asarray(M).T


def apply_matrix_lines(M, lines):
    return [apply_matrix(M, line) for line in lines]
