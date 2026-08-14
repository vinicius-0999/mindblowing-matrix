import numpy as np
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg
from matplotlib.figure import Figure

from core.eigen import compute_eigen, determinant, trace
from core.grid import base_vectors, grid_lines, unit_square
from core.transform import apply_matrix, apply_matrix_lines

GRID_EXTENT = 3


class MatrixCanvas(FigureCanvasQTAgg):
    def __init__(self):
        self.fig = Figure(figsize=(6, 6))
        super().__init__(self.fig)
        self.ax = self.fig.add_subplot(111)
        self.set_matrix(np.eye(2))

    def set_matrix(self, M):
        M = np.asarray(M, dtype=float)
        ax = self.ax
        ax.clear()

        lines = grid_lines(GRID_EXTENT)
        square = unit_square()
        e1, e2 = base_vectors()
        t_lines = apply_matrix_lines(M, lines)
        t_square = apply_matrix(M, square)
        t_e1 = M @ e1
        t_e2 = M @ e2

        for line in lines:
            ax.plot(line[:, 0], line[:, 1], color="#cccccc", linewidth=0.6, linestyle="--", zorder=1)
        ax.plot(square[:, 0], square[:, 1], color="#999999", linewidth=1, linestyle=":", zorder=1)

        for line in t_lines:
            ax.plot(line[:, 0], line[:, 1], color="#4c72b0", linewidth=0.9, zorder=2)
        ax.fill(t_square[:, 0], t_square[:, 1], color="#4c72b0", alpha=0.2, zorder=2)
        ax.plot(t_square[:, 0], t_square[:, 1], color="#4c72b0", linewidth=1.2, zorder=2)

        ax.annotate("", xy=t_e1, xytext=(0, 0),
                    arrowprops=dict(arrowstyle="->", color="#c44e52", lw=2), zorder=4)
        ax.annotate("", xy=t_e2, xytext=(0, 0),
                    arrowprops=dict(arrowstyle="->", color="#55a868", lw=2), zorder=4)

        _, real_eigen = compute_eigen(M)
        max_extent = GRID_EXTENT
        for val, vec in real_eigen:
            p = vec * GRID_EXTENT
            ax.plot([-p[0], p[0]], [-p[1], p[1]], color="#dd8452", linewidth=1.4,
                     linestyle="-.", zorder=3, label=f"autovetor (λ={val:.2f})")
            max_extent = max(max_extent, abs(val) * GRID_EXTENT)

        all_pts = np.vstack([t_square] + t_lines + [t_e1, t_e2])
        max_extent = max(max_extent, float(np.abs(all_pts).max()))
        limit = max_extent * 1.15
        ax.set_xlim(-limit, limit)
        ax.set_ylim(-limit, limit)
        ax.set_aspect("equal")
        ax.axhline(0, color="black", linewidth=0.5)
        ax.axvline(0, color="black", linewidth=0.5)
        if real_eigen:
            ax.legend(loc="upper left", fontsize=8)

        eigenvalues, _ = compute_eigen(M)
        eig_txt = ", ".join(self._format_eigenvalue(v) for v in eigenvalues)
        info = f"det = {determinant(M):.2f}   tr = {trace(M):.2f}\nautovalores: {eig_txt}"
        ax.set_title(info, fontsize=9, loc="left")

        self.draw()

    @staticmethod
    def _format_eigenvalue(v):
        if abs(v.imag) < 1e-9:
            return f"{v.real:.2f}"
        sign = "+" if v.imag >= 0 else "-"
        return f"{v.real:.2f} {sign} {abs(v.imag):.2f}i"
