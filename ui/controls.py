import numpy as np
from PySide6.QtCore import Signal
from PySide6.QtWidgets import (
    QCheckBox,
    QComboBox,
    QDoubleSpinBox,
    QGridLayout,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

PRESETS = {
    "Identidade": np.eye(2),
    "Rotação 90°": np.array([[0, -1], [1, 0]]),
    "Rotação 45°": np.array([[0.7071, -0.7071], [0.7071, 0.7071]]),
    "Escala 2x": np.array([[2, 0], [0, 2]]),
    "Cisalhamento X": np.array([[1, 1], [0, 1]]),
    "Reflexão eixo X": np.array([[1, 0], [0, -1]]),
    "Reflexão eixo Y": np.array([[-1, 0], [0, 1]]),
    "Projeção eixo X": np.array([[1, 0], [0, 0]]),
}


class MatrixControls(QWidget):
    matrixChanged = Signal(np.ndarray)
    animateRequested = Signal(np.ndarray)
    focusModeChanged = Signal(bool)

    def __init__(self):
        super().__init__()
        self._build_ui()
        self._emit_current()

    def _build_ui(self):
        layout = QVBoxLayout(self)

        layout.addWidget(QLabel("Matriz [[a, b], [c, d]]"))
        grid = QGridLayout()
        self.spin_a = self._make_spinbox(1.0)
        self.spin_b = self._make_spinbox(0.0)
        self.spin_c = self._make_spinbox(0.0)
        self.spin_d = self._make_spinbox(1.0)
        grid.addWidget(self.spin_a, 0, 0)
        grid.addWidget(self.spin_b, 0, 1)
        grid.addWidget(self.spin_c, 1, 0)
        grid.addWidget(self.spin_d, 1, 1)
        layout.addLayout(grid)

        layout.addWidget(QLabel("Predefinidas"))
        self.presets = QComboBox()
        self.presets.addItem("—")
        self.presets.addItems(PRESETS.keys())
        self.presets.currentTextChanged.connect(self._apply_preset)
        layout.addWidget(self.presets)

        reset_btn = QPushButton("Resetar p/ identidade")
        reset_btn.clicked.connect(lambda: self._apply_preset("Identidade"))
        layout.addWidget(reset_btn)

        animate_btn = QPushButton("Animar (identidade → matriz atual)")
        animate_btn.clicked.connect(lambda: self.animateRequested.emit(self.current_matrix()))
        layout.addWidget(animate_btn)

        self.focus_checkbox = QCheckBox("Modo foco: só o quadrado")
        self.focus_checkbox.setToolTip(
            "Grade, eixos e zoom fixos — só o quadrado sombreado muda com a matriz"
        )
        self.focus_checkbox.toggled.connect(self.focusModeChanged.emit)
        layout.addWidget(self.focus_checkbox)

        layout.addStretch()

    def _make_spinbox(self, initial):
        box = QDoubleSpinBox()
        box.setRange(-5.0, 5.0)
        box.setSingleStep(0.1)
        box.setDecimals(2)
        box.setValue(initial)
        box.valueChanged.connect(self._emit_current)
        return box

    def _apply_preset(self, name):
        if name not in PRESETS:
            return
        M = PRESETS[name]
        for box, val in zip(
            (self.spin_a, self.spin_b, self.spin_c, self.spin_d),
            (M[0, 0], M[0, 1], M[1, 0], M[1, 1]),
        ):
            box.blockSignals(True)
            box.setValue(val)
            box.blockSignals(False)
        self._emit_current()

    def current_matrix(self):
        return np.array(
            [
                [self.spin_a.value(), self.spin_b.value()],
                [self.spin_c.value(), self.spin_d.value()],
            ]
        )

    def _emit_current(self):
        self.matrixChanged.emit(self.current_matrix())
