import numpy as np
from sklearn.metrics import accuracy_score, cohen_kappa_score
from sklearn.cross_validation import cross_val_predict, StratifiedKFold


def cross_val_scores(clf, X, y, n_iters=10, n_folds=10, n_jobs=1):
    scores = np.zeros((n_iters, 2))
    for iter in range(n_iters):
        # random_state=iter to control the randomness for reproducibility
        cv = StratifiedKFold(y, n_folds, shuffle=True, random_state=iter)
        y_pred = cross_val_predict(clf, X, y, cv, n_jobs=n_jobs)
        scores[iter, 0] = accuracy_score(y, y_pred)
        scores[iter, 1] = cohen_kappa_score(y, y_pred)

    return (scores[:,0].mean(), scores[:,0].std(),
            scores[:,1].mean(), scores[:,1].std())
