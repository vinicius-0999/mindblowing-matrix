from PySide6.QtWidgets import QHBoxLayout, QMainWindow, QWidget

from plotting.animate import MatrixAnimator
from plotting.canvas import MatrixCanvas
from ui.controls import MatrixControls


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Matriz Visual — transformações lineares em R²")
        self.resize(1000, 650)

        self.controls = MatrixControls()
        self.canvas = MatrixCanvas()
        self.animator = MatrixAnimator(self.canvas)

        self.controls.matrixChanged.connect(self.canvas.set_matrix)
        self.controls.animateRequested.connect(self.animator.animate_to)

        central = QWidget()
        layout = QHBoxLayout(central)
        layout.addWidget(self.controls, stretch=0)
        layout.addWidget(self.canvas, stretch=1)
        self.setCentralWidget(central)
