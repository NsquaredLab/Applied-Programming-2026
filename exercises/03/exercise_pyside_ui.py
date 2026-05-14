# Copyright 2026 n-squared LAB @ FAU Erlangen-Nuernberg

"""
Exercise 3 - PySide6 UI with Embedded Matplotlib

- Channel selection (dropdown)
- Signal type selection (dropdown)
- Plot color change (button)
- Auto-updating plot

Students should complete the TODO sections.
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

        # TODO 1:
        # Set the window title to "EMG Signal Viewer"
        self.setWindowTitle("EMG Signal Viewer")
        # Set the window size to 1000 x 700
        self.resize(1000, 700)
        # self.setWindowTitle(...)
        
        # self.resize(...)
        

        # Central widget
        # TODO 2:
        # Create a QWidget called central_widget
        central_widget = QWidget()
        # Set it as the central widget of the main window
        # central_widget = ...
        self.setCentralWidget(central_widget)
        # self.setCentralWidget(...)

        # Layouts
        # TODO 3:
        # Create:
        # - a vertical layout called main_layout attached to central_widget
        # - a horizontal layout called controls_layout
        # main_layout = ...
        main_layout = QVBoxLayout(central_widget)
        # controls_layout = ...
        controls_layout = QHBoxLayout()

        # Channel selector
        # TODO 4:
        # Create:
        # - QLabel("Channel:")
        label = QLabel("Channel:")
        # - QComboBox()
        combo = QComboBox()
        # Fill the combo box with "Channel 1", "Channel 2", ...
        combo.addItems([f"Channel {i+1}" for i in range(self.channel_data.shape[0])])
        self.channel_label = label
        self.channel_combo = combo

        # Signal selector
        # TODO 5:
        # Create:
        # - QLabel("Signal:")
        label = QLabel("Signal:")
        # - QComboBox()
        combo = QComboBox()
        # Add the items ["Original", "Filtered", "RMS"]
        combo.addItems(["Original", "Filtered", "RMS"])
        self.signal_label = label
        self.signal_combo = combo

        # Button: change color
        # TODO 6:
        # Create a QPushButton with the text "Change Color"
        self.color_button = QPushButton("Change Color")

        # Add controls
        # TODO 7:
        # Add the widgets to controls_layout in this order:
        controls_layout.addWidget(self.channel_label)
        controls_layout.addWidget(self.channel_combo)
        controls_layout.addWidget(self.signal_label)
        controls_layout.addWidget(self.signal_combo)
        controls_layout.addWidget(self.color_button)

        # TODO 8:
        # Add controls_layout to main_layout
        main_layout.addLayout(controls_layout)

        # Matplotlib
        # TODO 9:
        # Create:
        # - a Figure with figsize=(8, 5)
        fig = Figure(figsize=(8, 5))
        # - a FigureCanvas from that figure
        canvas = FigureCanvas(fig)
        # - one subplot using add_subplot(111)
        ax = fig.add_subplot(111)

        self.figure = fig
        self.canvas = canvas
        self.ax = ax

        # TODO 10:
        # Add the canvas to main_layout
        main_layout.addWidget(self.canvas)

        # Connections
        # TODO 11:
        # Connect:
        # - channel_combo.currentIndexChanged -> self.update_plot
        self.channel_combo.currentIndexChanged.connect(self.update_plot)
        # - signal_combo.currentIndexChanged -> self.update_plot
        self.signal_combo.currentIndexChanged.connect(self.update_plot)
        # - color_button.clicked -> self.change_color
        self.color_button.clicked.connect(self.change_color)

        # TODO 12:
        # Call self.update_plot() once so an initial plot appears
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
    filename = r"C:/Users/hcgut/Documents/Applied-Programming-2026/recording.pkl"

    emg_signal, sampling_rate = load_emg_data(filename)
    channel_data = restructure_emg_data(emg_signal)

    app = QApplication(sys.argv)
    window = EMGViewer(channel_data, sampling_rate)
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
