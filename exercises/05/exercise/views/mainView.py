from PySide6.QtWidgets import (
    QDoubleSpinBox,
    QLabel,
    QMainWindow,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QWidget,
)

from views.plotView import VisPyPlotWidget


class MainView(QMainWindow):
    """
    Main application window.

    The View owns the visible widgets:
    - signal time label
    - y-scale input
    - plot widget
    - start/stop button

    The View does not receive TCP data directly.
    It only connects ViewModel signals to visible widgets.
    """

    def __init__(self, view_model):
        super().__init__()

        self.view_model = view_model

        self.setWindowTitle("TCP EMG Viewer")
        self.resize(1200, 800)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(8, 8, 8, 8)
        main_layout.setSpacing(8)

        self.time_label = QLabel("Signal time: 0.00 s")
        self.time_label.setStyleSheet("font-size: 18px; font-weight: bold;")

        content_layout = QHBoxLayout()
        content_layout.setSpacing(8)

        control_layout = QVBoxLayout()
        control_layout.setSpacing(8)

        self.y_scale_label = QLabel("Y scale")
        self.y_scale_input = QDoubleSpinBox()
        self.y_scale_input.setRange(0.01, 100000.0)
        self.y_scale_input.setValue(300.0)
        self.y_scale_input.setSingleStep(50.0)
        self.y_scale_input.setDecimals(2)

        self.info_label = QLabel("Start the TCP server first.")
        self.toggle_button = QPushButton("Start Plotting")

        control_layout.addWidget(self.y_scale_label)
        control_layout.addWidget(self.y_scale_input)
        control_layout.addStretch()
        control_layout.addWidget(self.info_label)
        control_layout.addWidget(self.toggle_button)

        self.plot_widget = VisPyPlotWidget(
            visible_duration_seconds=10.0,
            y_scale=self.y_scale_input.value(),
        )

        content_layout.addLayout(control_layout, stretch=0)
        content_layout.addWidget(self.plot_widget, stretch=1)

        main_layout.addWidget(self.time_label)
        main_layout.addLayout(content_layout)

        self.toggle_button.clicked.connect(self.toggle_plotting)
        self.y_scale_input.valueChanged.connect(self.plot_widget.set_y_scale)

        self.view_model.plot_updated.connect(self.plot_widget.update_plot)
        self.view_model.status_updated.connect(self.info_label.setText)
        self.view_model.signal_time_updated.connect(self.update_signal_time)
        self.view_model.signal_time_updated.connect(self.plot_widget.set_signal_time)

    def toggle_plotting(self):
        if self.view_model.is_plotting:
            self.view_model.stop_plotting()
            self.toggle_button.setText("Start Plotting")
        else:
            self.view_model.start_plotting()

            if self.view_model.is_plotting:
                self.toggle_button.setText("Stop Plotting")

    def update_signal_time(self, signal_time_seconds):
        self.time_label.setText(f"Signal time: {signal_time_seconds:.2f} s")
