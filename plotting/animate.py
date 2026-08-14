import numpy as np
from PySide6.QtCore import QTimer


class MatrixAnimator:
    def __init__(self, canvas):
        self.canvas = canvas
        self.timer = QTimer()
        self.timer.timeout.connect(self._step)
        self.target = None
        self.step_i = 0
        self.steps = 30

    def animate_to(self, M, steps=30, interval_ms=20):
        self.timer.stop()
        self.target = np.asarray(M, dtype=float)
        self.steps = steps
        self.step_i = 0
        self.timer.start(interval_ms)

    def _step(self):
        self.step_i += 1
        t = self.step_i / self.steps
        M_t = (1 - t) * np.eye(2) + t * self.target
        self.canvas.set_matrix(M_t)
        if self.step_i >= self.steps:
            self.timer.stop()
