import numpy as np
from mne.decoding import CSP
from sklearn.pipeline import Pipeline, FeatureUnion
from .band_pass_filter import BandPassFilter


def create_band_list(start_freq=8, n_filters=10, band_overlap=2, bandwidth=4):
    if band_overlap >= bandwidth:
        raise ValueError("Band overlap (%s) can not be equal to or greater "
                         "than band width (%s)" % (band_overlap, bandwidth))
    step = bandwidth - band_overlap
    low_freqs = range(start_freq, start_freq + n_filters * step, step)
    bands = []
    for low_freq in low_freqs:
        bands.append(low_freq)
        bands.append(low_freq + bandwidth)
    return np.array(bands)

def create_fbcsp(bands, n_components=2, transform_into="average_power"):
    pipeline = []
    for low, high in zip(bands[::2], bands[1::2]):
        pipeline.append(
            ("pipe", Pipeline([
                ("bandpass_filter", BandPassFilter(low, high)),
                ("csp", CSP(n_components=n_components,
                            transform_into=transform_into))
            ]))
        )
    return FeatureUnion(pipeline)
