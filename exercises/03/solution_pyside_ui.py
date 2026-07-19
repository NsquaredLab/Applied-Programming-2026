# Copyright 2026 n-squared LAB @ FAU Erlangen-Nuernberg

"""
Solution - Exercise 3: PySide6 UI with Embedded Matplotlib

- Channel selection (dropdown)
- Signal type selection (dropdown)
- Plot color change (button)
- Auto-updating plot
"""

import sys
import numpy as np
import pandas as pd
from scipy import signal

from PySide6.QtWidgets import (
    QApplication,
    QComboBox,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure


# ======================
# Data Processing
# ======================

def load_emg_data(filename: str):
    data = pd.read_pickle(filename)
    emg_signal = data["biosignal"]
    sampling_rate = data["device_information"]["sampling_frequency"]
    return emg_signal, sampling_rate


def restructure_emg_data(emg_signal: np.ndarray):
    num_channels = emg_signal.shape[0]
    channel_data = emg_signal.transpose(2, 1, 0).reshape(-1, num_channels).T
    return channel_data


def bandpass_filter_channel(channel: np.ndarray, sampling_rate: float):
    nyquist = sampling_rate / 2
    low = 20 / nyquist
    high = 450 / nyquist
    b, a = signal.butter(4, [low, high], btype="band")
    return signal.filtfilt(b, a, channel)


def compute_rms_channel(channel: np.ndarray, sampling_rate: float):
    window_size = int(0.1 * sampling_rate)
    kernel = np.ones(window_size) / window_size
    squared = channel ** 2
    mean_squared = np.convolve(squared, kernel, mode="same")
    return np.sqrt(mean_squared)


# ======================
# UI
# ======================

class EMGViewer(QMainWindow):
    def __init__(self, channel_data, sampling_rate):
        super().__init__()

        self.channel_data = channel_data
        self.sampling_rate = sampling_rate

        self.colors = ["blue", "red", "green", "black"]
        self.color_index = 0

        self.setWindowTitle("EMG Signal Viewer")
        self.resize(1000, 700)

        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Layouts
        main_layout = QVBoxLayout(central_widget)
        controls_layout = QHBoxLayout()

        # Channel selector
        self.channel_label = QLabel("Channel:")
        self.channel_combo = QComboBox()
        self.channel_combo.addItems(
            [f"Channel {i+1}" for i in range(channel_data.shape[0])]
        )

        # Signal selector
        self.signal_label = QLabel("Signal:")
        self.signal_combo = QComboBox()
        self.signal_combo.addItems(["Original", "Filtered", "RMS"])

        # Button: change color
        self.color_button = QPushButton("Change Color")

        # Add controls
        controls_layout.addWidget(self.channel_label)
        controls_layout.addWidget(self.channel_combo)
        controls_layout.addWidget(self.signal_label)
        controls_layout.addWidget(self.signal_combo)
        controls_layout.addWidget(self.color_button)

        main_layout.addLayout(controls_layout)

        # Matplotlib
        self.figure = Figure(figsize=(8, 5))
        self.canvas = FigureCanvas(self.figure)
        self.ax = self.figure.add_subplot(111)

        main_layout.addWidget(self.canvas)

        # Connections
        self.channel_combo.currentIndexChanged.connect(self.update_plot)
        self.signal_combo.currentIndexChanged.connect(self.update_plot)
        self.color_button.clicked.connect(self.change_color)

        self.update_plot()

    # ======================
    # Logic
    # ======================

    def change_color(self):
        self.color_index = (self.color_index + 1) % len(self.colors)
        self.update_plot()

    def update_plot(self):
        ch = self.channel_combo.currentIndex()
        signal_type = self.signal_combo.currentText()

        raw = self.channel_data[ch, :]
        t = np.arange(len(raw)) / self.sampling_rate

        if signal_type == "Original":
            y = raw
        elif signal_type == "Filtered":
            y = bandpass_filter_channel(raw, self.sampling_rate)
        else:
            y = compute_rms_channel(raw, self.sampling_rate)

        color = self.colors[self.color_index]

        self.ax.clear()
        self.ax.plot(t, y, color=color)
        self.ax.set_title(f"{signal_type} - Channel {ch+1}")
        self.ax.set_xlabel("Time (s)")
        self.ax.set_ylabel("Amplitude")
        self.ax.grid(True)

        self.canvas.draw()


# ======================
# Main
# ======================

def main():
    filename = "D:/PhD/Teaching/Applied-Programming-2026/Applied-Programming-2026/recording.pkl"

    emg_signal, sampling_rate = load_emg_data(filename)
    channel_data = restructure_emg_data(emg_signal)

    app = QApplication(sys.argv)
    window = EMGViewer(channel_data, sampling_rate)
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
