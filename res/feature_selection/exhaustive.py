import numpy as np
from itertools import chain, combinations
from sklearn.base import BaseEstimator, clone
from sklearn.feature_selection.base import SelectorMixin

from util import cross_val_scores


class Exhaustive(BaseEstimator, SelectorMixin):

    def __init__(self, estimator, n_components=2, n_bands=4):
        self.estimator = estimator
        self.n_components = n_components
        self.n_bands_to_select = n_bands

    def _get_support_mask(self):
        mask = np.full(self.n_features, False, dtype=np.bool)

        for feature in self.selected_features:
            mask[feature] = True

        return mask

    def fit(self, X, y=None):
        """Fit the FeatureSelector transformer.
        Parameters
        ----------
        X : array-like of shape (n_samples, n_features)
            The training input samples.
        y : array-like, shape (n_samples,)
        Returns
        -------
        self : object
            Returns self.
        """

        self.n_features = X.shape[1]
        CSP_features = list(range(self.n_features))
        CSP_features = list(zip(*[iter(CSP_features)] * self.n_components))
       
        band_combinations = list(combinations(CSP_features, self.n_bands_to_select))
        acc_scores = np.zeros(len(band_combinations))
        kap_scores = np.zeros(len(band_combinations))
        acc_std = np.zeros(len(band_combinations))
        kap_std = np.zeros(len(band_combinations))
        for i, bands in enumerate(band_combinations):
            feat_subset = list(chain(*bands))
            estimator = clone(self.estimator)
            acc_scores[i], acc_std[i], kap_scores[i], kap_std[i] = \
                cross_val_scores(estimator, X[:, feat_subset], y)
       
        arg_max = np.argmax(acc_scores)
        self.accur_score = acc_scores[arg_max] * 100
        self.kappa_score = kap_scores[arg_max]
        self.accur_std = acc_std[arg_max] * 100
        self.kappa_std = kap_std[arg_max]
        self.selected_bands = [int(feats[0]/self.n_components) \
                               for feats in band_combinations[arg_max]]
        self.selected_features = list(chain(*band_combinations[arg_max]))
        return self
