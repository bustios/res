import numpy as np
import scipy.signal as signal
import matplotlib.pyplot as plt


class RawEpochs:

    def __init__(self, X, y, sfreq=250, start_at=499, low_freq=0.5, high_freq=100.):
        self.raw_epochs = X  # numpy array
        self.y = y  # class labels of the epochs
        self.sfreq = int(sfreq)  # sampling frequency
        self.nyquist = sfreq / 2
        self.start_at = start_at
        self.low_freq = low_freq
        self.high_freq = high_freq
        self.n_epochs = X.shape[0]
        self.n_channels = X.shape[1]
        self.n_samples = X.shape[2] - self.start_at  # valid samples
        self.length = self.n_samples // self.sfreq  # epochs length in secs

    def window(self, start_time, win_len):
        start = int(self.sfreq * start_time + self.start_at)
        if win_len > 0:
            end = start + int(self.sfreq * win_len)
        else:
            end = start + 1
            start = start - self.start_at
        return self.raw_epochs[:, :, start:end]
