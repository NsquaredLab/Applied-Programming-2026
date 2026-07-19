import numpy as np


class SignalModel:
    """
    Model class responsible for creating and serving signal data.

    In this exercise, the signal is simulated locally.
    Later, this role can be replaced or extended by a TCP-based model.
    """

    def __init__(self, sampling_rate=1000, duration=10, window_size=1000, step_size=50):
        self.sampling_rate = sampling_rate
        self.duration = duration
        self.window_size = window_size
        self.step_size = step_size

        self.t = np.linspace(0, duration, int(sampling_rate * duration), endpoint=False)

        # Simulated EMG-like signal: sine + noise
        self.signal = np.sin(0.2 * np.pi * 5 * self.t) + 0.2 * np.random.randn(len(self.t))

    def get_window(self, start_idx):
        """
        Return one sliding window of data.

        Parameters
        ----------
        start_idx : int
            Start index of the window.

        Returns
        -------
        tuple[np.ndarray, np.ndarray]
            time window and signal window
        """
        end_idx = start_idx + self.window_size
        return self.t[start_idx:end_idx], self.signal[start_idx:end_idx]

    def has_enough_data(self, start_idx):
        """Check whether a full window can still be extracted."""
        return start_idx + self.window_size <= len(self.signal)
