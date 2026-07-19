from PySide6.QtWidgets import QLabel, QMainWindow, QPushButton, QVBoxLayout, QWidget

from views.plotView import VisPyPlotWidget


class MainView(QMainWindow):
    def __init__(self, view_model):
        super().__init__()

        self.view_model = view_model

        self.setWindowTitle("VisPy EMG Viewer")
        self.resize(1200, 800)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout(central_widget)
        layout.setContentsMargins(8, 8, 8, 8)
        layout.setSpacing(6)

        self.info_label = QLabel("Press 'Start Plotting' to begin.")
        self.plot_widget = VisPyPlotWidget()
        self.toggle_button = QPushButton("Start Plotting")

        layout.addWidget(self.info_label)
        layout.addWidget(self.plot_widget, stretch=1)
        layout.addWidget(self.toggle_button)

        self.toggle_button.clicked.connect(self.toggle_plotting)
        self.view_model.plot_updated.connect(self.plot_widget.update_plot)

    def toggle_plotting(self):
        if self.view_model.is_plotting:
            self.view_model.stop_plotting()
            self.toggle_button.setText("Start Plotting")
            self.info_label.setText("Plotting stopped.")
        else:
            self.view_model.start_plotting()
            self.toggle_button.setText("Stop Plotting")
            self.info_label.setText("Plotting running...")