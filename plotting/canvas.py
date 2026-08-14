import numpy as np
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg
from matplotlib.figure import Figure

from core.eigen import compute_eigen, determinant, trace
from core.grid import base_vectors, grid_lines, unit_square
from core.transform import apply_matrix, apply_matrix_lines

BASE_EXTENT = 3  # extensão de referência do modo completo (matriz perto da identidade)
FOCUS_BASE_LIMIT = 5  # viewport do modo foco antes do zoom
ZOOM_FACTOR = 1.25
ZOOM_MIN, ZOOM_MAX = 0.15, 8.0
# espaçamentos "redondos" candidatos pra grade, do mais fino ao mais grosso
NICE_STEPS = [0.1, 0.2, 0.5, 1, 2, 5, 10, 20, 50, 100]


def _nice_step(extent, target_lines=10):
    """Espaçamento de grade que mantém ~target_lines linhas visíveis em qualquer zoom
    — sem isso, dar zoom out deixa a grade rala e zoom in deixa ela lotada demais."""
    raw = (2 * extent) / target_lines
    for step in NICE_STEPS:
        if step >= raw:
            return step
    return NICE_STEPS[-1]


class MatrixCanvas(FigureCanvasQTAgg):
    def __init__(self):
        self.fig = Figure(figsize=(6, 6))
        super().__init__(self.fig)
        self.ax = self.fig.add_subplot(111)
        self.focus_mode = False
        self.zoom_scale = 1.0
        self.last_matrix = np.eye(2)
        self.mpl_connect("scroll_event", self._on_scroll)
        self.set_matrix(self.last_matrix)

    def set_focus_mode(self, enabled):
        self.focus_mode = enabled
        self.set_matrix(self.last_matrix)

    def zoom_in(self):
        self.zoom_scale = max(ZOOM_MIN, self.zoom_scale / ZOOM_FACTOR)
        self.set_matrix(self.last_matrix)

    def zoom_out(self):
        self.zoom_scale = min(ZOOM_MAX, self.zoom_scale * ZOOM_FACTOR)
        self.set_matrix(self.last_matrix)

    def zoom_reset(self):
        self.zoom_scale = 1.0
        self.set_matrix(self.last_matrix)

    def _on_scroll(self, event):
        if event.step > 0:
            self.zoom_in()
        elif event.step < 0:
            self.zoom_out()

    def set_matrix(self, M):
        M = np.asarray(M, dtype=float)
        self.last_matrix = M
        ax = self.ax
        ax.clear()

        square = unit_square()
        t_square = apply_matrix(M, square)

        if self.focus_mode:
            self._draw_focus(ax, M, square, t_square)
        else:
            self._draw_full(ax, M, square, t_square)

        eigenvalues, _ = compute_eigen(M)
        eig_txt = ", ".join(self._format_eigenvalue(v) for v in eigenvalues)
        info = f"det = {determinant(M):.2f}   tr = {trace(M):.2f}\nautovalores: {eig_txt}"
        ax.set_title(info, fontsize=9, loc="left")

        self.draw()

    def _draw_grid(self, ax, extent, **kwargs):
        style = dict(color="#cccccc", linewidth=0.6, linestyle="--", zorder=1)
        style.update(kwargs)
        for line in grid_lines(extent, _nice_step(extent)):
            ax.plot(line[:, 0], line[:, 1], **style)

    def _draw_eigenvectors(self, ax, M, limit):
        _, real_eigen = compute_eigen(M)
        for val, vec in real_eigen:
            p = vec * limit
            ax.plot([-p[0], p[0]], [-p[1], p[1]], color="#dd8452", linewidth=1.4,
                     linestyle="-.", zorder=3, label=f"autovetor (λ={val:.2f})")
        if real_eigen:
            ax.legend(loc="upper left", fontsize=8)

    def _finish_axes(self, ax, limit):
        ax.set_xlim(-limit, limit)
        ax.set_ylim(-limit, limit)
        ax.set_aspect("equal")
        ax.axhline(0, color="black", linewidth=0.5)
        ax.axvline(0, color="black", linewidth=0.5)

    def _draw_full(self, ax, M, square, t_square):
        e1, e2 = base_vectors()
        t_e1 = M @ e1
        t_e2 = M @ e2

        _, real_eigen = compute_eigen(M)
        max_extent = BASE_EXTENT
        for val, _vec in real_eigen:
            max_extent = max(max_extent, abs(val) * BASE_EXTENT)
        all_pts = np.vstack([t_square, t_e1, t_e2])
        max_extent = max(max_extent, float(np.abs(all_pts).max()))
        limit = max_extent * 1.15 * self.zoom_scale

        self._draw_grid(ax, limit)
        ax.plot(square[:, 0], square[:, 1], color="#999999", linewidth=1, linestyle=":", zorder=1)

        t_lines = apply_matrix_lines(M, grid_lines(limit, _nice_step(limit)))
        for line in t_lines:
            ax.plot(line[:, 0], line[:, 1], color="#4c72b0", linewidth=0.9, zorder=2)
        ax.fill(t_square[:, 0], t_square[:, 1], color="#4c72b0", alpha=0.2, zorder=2)
        ax.plot(t_square[:, 0], t_square[:, 1], color="#4c72b0", linewidth=1.2, zorder=2)

        ax.annotate("", xy=t_e1, xytext=(0, 0),
                    arrowprops=dict(arrowstyle="->", color="#c44e52", lw=2), zorder=4)
        ax.annotate("", xy=t_e2, xytext=(0, 0),
                    arrowprops=dict(arrowstyle="->", color="#55a868", lw=2), zorder=4)

        self._draw_eigenvectors(ax, M, limit)
        self._finish_axes(ax, limit)

    def _draw_focus(self, ax, M, square, t_square):
        # grade, eixos e viewport fixos (exceto zoom manual) — só o quadrado sombreado
        # e os autovetores mudam, pra isolar visualmente o efeito da matriz
        limit = FOCUS_BASE_LIMIT * self.zoom_scale

        self._draw_grid(ax, limit)
        ax.plot(square[:, 0], square[:, 1], color="#999999", linewidth=1.2, linestyle=":", zorder=1)

        ax.fill(t_square[:, 0], t_square[:, 1], color="#4c72b0", alpha=0.35, zorder=2)
        ax.plot(t_square[:, 0], t_square[:, 1], color="#4c72b0", linewidth=2, zorder=3)

        self._draw_eigenvectors(ax, M, limit)
        self._finish_axes(ax, limit)

    @staticmethod
    def _format_eigenvalue(v):
        if abs(v.imag) < 1e-9:
            return f"{v.real:.2f}"
        sign = "+" if v.imag >= 0 else "-"
        return f"{v.real:.2f} {sign} {abs(v.imag):.2f}i"
