from PySide6.QtWidgets import QVBoxLayout, QWidget
from vispy import scene
import numpy as np


class VisPyPlotWidget(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        self.canvas = scene.SceneCanvas(
            keys="interactive",
            show=False,
            bgcolor="white",
            size=(1000, 600),
        )

        grid = self.canvas.central_widget.add_grid(margin=10)

        self.y_axis = scene.AxisWidget(orientation="left")
        self.x_axis = scene.AxisWidget(orientation="bottom")

        self.y_axis.width_max = 50
        self.x_axis.height_max = 40

        grid.add_widget(self.y_axis, row=0, col=0)

        self.view = grid.add_view(row=0, col=1)
        self.view.camera = "panzoom"

        grid.add_widget(self.x_axis, row=1, col=1)

        self.x_axis.link_view(self.view)
        self.y_axis.link_view(self.view)

        self.line = scene.Line(
            pos=np.array([[0.0, 0.0], [1.0, 0.0]], dtype=float),
            color=(0.1, 0.3, 0.8, 1.0),
            parent=self.view.scene,
            width=2,
        )

        layout.addWidget(self.canvas.native)

    def update_plot(self, x, y):
        x = np.asarray(x, dtype=float)
        y = np.asarray(y, dtype=float)

        # TODO 1:
        # Combine x and y into an (N, 2) position array.
        pos = None

        # TODO 2:
        # Update the line data with the new positions.

        y_pad = max(0.1, 0.1 * (y.max() - y.min() + 1e-9))

        # TODO 3:
        # Update the camera range so the current data window is visible.
        # Use:
        # - x min/max
        # - y min/max with padding