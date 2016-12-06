import numpy as np
from itertools import chain, combinations
from sklearn.base import BaseEstimator, clone
from sklearn.feature_selection.base import SelectorMixin

from util import cross_val_scores


class Sffs(BaseEstimator, SelectorMixin):

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
        selected_k_pairs = []  # X_k
        selected_k_1_pairs = []  # X_k_1
        J_X_i = np.zeros(self.n_bands_to_select)
        J_X_k_1 = 0
        
        while len(selected_k_pairs) < self.n_bands_to_select:
            acc_scores = np.zeros(len(CSP_features))
            kap_scores = np.zeros(len(CSP_features))
            acc_std = np.zeros(len(CSP_features))
            kap_std = np.zeros(len(CSP_features))
            
            for i, x_k_1 in enumerate(CSP_features):
                feat_subset = selected_k_pairs.copy()
                feat_subset.append(x_k_1)
                feat_subset = list(chain(*feat_subset))
                estimator = clone(self.estimator)
                acc_scores[i], acc_std[i], kap_scores[i], kap_std[i] = \
                    cross_val_scores(estimator, X[:, feat_subset], y)

            arg_max = np.argmax(acc_scores)
            kappa_score = kap_scores[arg_max]
            accur_std = acc_std[arg_max]
            kappa_std = kap_std[arg_max]
            J_X_k_1 = acc_scores[arg_max]
            x_k_1 = CSP_features.pop(arg_max)
            selected_k_1_pairs.append(x_k_1)
            
            while len(selected_k_1_pairs) > 2:
                # J(X_k_1) >= J(X_k_1 - x_j)   j = 1, 2, ..., k
                r = len(selected_k_1_pairs) - 1
                band_combinations = list(combinations(selected_k_1_pairs, r))
                n_combinations = len(band_combinations)
                acc_scores = np.zeros(n_combinations)
                kap_scores = np.zeros(n_combinations)
                acc_std = np.zeros(n_combinations)
                kap_std = np.zeros(n_combinations)
                for j, bands in enumerate(band_combinations):
                    estimator = clone(self.estimator)
                    subset = list(chain(*bands))
                    acc_scores[j], acc_std[j], kap_scores[j], kap_std[j] = \
                        cross_val_scores(estimator, X[:, subset], y)

                # if J(X_k_1 - x_r) > J(X_k)
                if acc_scores.max() > J_X_i[r-1]:
                    arg_max = np.argmax(acc_scores)
                    x_r = list(set(selected_k_1_pairs) - 
                               set(band_combinations[arg_max]))[0]
                    CSP_features.append(x_r)
                    selected_k_1_pairs.remove(x_r)
                    J_X_k_1 = acc_scores[arg_max]
                    kappa_score = kap_scores[arg_max]
                    accur_std = acc_std[arg_max]
                    kappa_std = kap_std[arg_max]

                else:
                    break
            
            selected_k_pairs = selected_k_1_pairs.copy()
            J_X_i[len(selected_k_pairs) - 1] = J_X_k_1

        self.accur_score = J_X_i[-1] * 100
        self.kappa_score = kappa_score
        self.accur_std = accur_std * 100
        self.kappa_std = kappa_std
        self.selected_bands = [int(feats[0]/self.n_components) \
                               for feats in selected_k_pairs]
        self.selected_features = list(chain(*selected_k_pairs))
        return self
