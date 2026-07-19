from PySide6.QtCore import QObject, QTimer, Signal

from models.tcp_client_model import TcpClientModel


class MainViewModel(QObject):
    """
    ViewModel for the TCP live plotting exercise.

    Responsibilities:
    - create the TCP client model
    - connect/disconnect from the server
    - use a QTimer to regularly ask the model for new data
    - emit x/y plot data to the View
    - emit the current signal time to the View
    """

    plot_updated = Signal(object, object)
    status_updated = Signal(str)
    signal_time_updated = Signal(float)

    def __init__(self):
        super().__init__()

        self.model = TcpClientModel(
            host="localhost",
            port=12345,
            sampling_rate=2000,
            channels=32,
            samples_per_packet=18,
            window_seconds=10,
            selected_channel=1,
        )

        self.is_plotting = False

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_plot)

    def start_plotting(self):
        """Connect to the server and start updating the plot."""
        if self.is_plotting:
            return

        try:
            self.model.connect()
        except OSError as error:
            self.status_updated.emit(f"Could not connect to server: {error}")
            return

        self.is_plotting = True
        self.status_updated.emit("Connected to TCP server.")
        self.timer.start(10)

    def stop_plotting(self):
        """Stop updating the plot and close the TCP connection."""
        if not self.is_plotting:
            return

        self.timer.stop()
        self.model.disconnect()

        self.is_plotting = False
        self.status_updated.emit("Disconnected from TCP server.")

    def update_plot(self):
        """
        Receive new TCP data and emit it to the View.

        This method is called repeatedly by the QTimer.
        """
        self.model.receive_data()

        if not self.model.has_data():
            return

        x, y = self.model.get_window()
        self.plot_updated.emit(x, y)

        signal_time = self.model.get_signal_time_seconds()
        self.signal_time_updated.emit(signal_time)
