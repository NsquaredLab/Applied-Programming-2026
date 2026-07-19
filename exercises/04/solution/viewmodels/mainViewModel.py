from PySide6.QtCore import QObject, QTimer, Signal

from models.signal_model import SignalModel


class MainViewModel(QObject):
    plot_updated = Signal(object, object)

    def __init__(self):
        super().__init__()

        self.model = SignalModel(
            sampling_rate=1000,
            duration=100,
            window_size=5000,
            step_size=20,
        )
        self.current_index = 0
        self.is_plotting = False

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_plot)

    def start_plotting(self):
        if not self.is_plotting:
            self.is_plotting = True
            self.timer.start(10)

    def stop_plotting(self):
        if self.is_plotting:
            self.is_plotting = False
            self.timer.stop()

    def update_plot(self):
        if not self.model.has_enough_data(self.current_index):
            self.current_index = 0

        x, y = self.model.get_window(self.current_index)
        self.plot_updated.emit(x, y)

        self.current_index += self.model.step_size