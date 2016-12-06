from scipy.signal import filtfilt, iirdesign
from sklearn.base import BaseEstimator, TransformerMixin


class BandPassFilter(BaseEstimator, TransformerMixin):

    def __init__(self, low_freq=7., high_freq=30., gpass=0.5, gstop=10.,
                 sfreq=250, ftype="cheby2"):
        nyquist = sfreq / 2.
        wp = [low_freq / nyquist, high_freq / nyquist]
        ws = [(low_freq - 0.5) / nyquist, (high_freq + 0.5) / nyquist]
        self.b, self.a = iirdesign(wp, ws, gpass, gstop, ftype=ftype)

    def fit(self, X, y=None):
        """Just for sklearn.pipeline.Pipeline sklearn compatibility.

        Parameters
        ----------
        X : any
            Ignored. This parameter exists only for compatibility with
            sklearn.pipeline.Pipeline.
        y : any
            Ignored. This parameter exists only for compatibility with
            sklearn.pipeline.Pipeline.
        Returns
        -------
        self : object
            Returns the instance itself.
        """
        return self

    def transform(self, X, y=None):
        """Bandpass filter for the signal X.

        Applies a zero-phase bandpass filter to the signal X, operating on the
        last dimension.

        Parameters
        ----------
        X : array-like, shape (n_epochs, n_channels, n_time_samples)
            The array of data to be filtered.
        y : None
            Not used.
        Returns
        -------
        X_filtered : ndarray of shape (n_epochs, n_channels, n_time_samples)
            The data filtered.
        """
        return filtfilt(self.b, self.a, X)

