import numpy as np


def grid_lines(extent=3, step=1):
    """Linhas da malha cartesiana em [-extent, extent], cada uma como par de pontos
    (transformação linear leva reta em reta, então dois pontos bastam).

    As posições partem de 0 e crescem pra cada lado — se ancorasse em -extent, um step
    que não divide extent certinho desalinharia a grade da origem (ela pareceria "nascer"
    do canto da tela em vez de ficar centrada em x=0/y=0)."""
    positive = np.arange(0, extent + step, step)
    offsets = np.union1d(-positive, positive)
    offsets = offsets[np.abs(offsets) <= extent + 1e-9]

    lines = []
    for x in offsets:
        lines.append(np.array([[x, -extent], [x, extent]]))
    for y in offsets:
        lines.append(np.array([[-extent, y], [extent, y]]))
    return lines


def unit_square():
    return np.array([[0, 0], [1, 0], [1, 1], [0, 1], [0, 0]], dtype=float)


def base_vectors():
    return np.array([1.0, 0.0]), np.array([0.0, 1.0])
