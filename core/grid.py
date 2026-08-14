import numpy as np


def grid_lines(extent=3, step=1):
    """Linhas da malha cartesiana em [-extent, extent], cada uma como par de pontos
    (transformação linear leva reta em reta, então dois pontos bastam)."""
    lines = []
    for x in np.arange(-extent, extent + step, step):
        lines.append(np.array([[x, -extent], [x, extent]]))
    for y in np.arange(-extent, extent + step, step):
        lines.append(np.array([[-extent, y], [extent, y]]))
    return lines


def unit_square():
    return np.array([[0, 0], [1, 0], [1, 1], [0, 1], [0, 0]], dtype=float)


def base_vectors():
    return np.array([1.0, 0.0]), np.array([0.0, 1.0])
