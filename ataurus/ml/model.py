import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.base import BaseEstimator, ClassifierMixin
from sklearn.metrics import f1_score
from sklearn.impute import SimpleImputer


class Model(BaseEstimator, ClassifierMixin):
    def __init__(self, estimator='RandomForest', remove_nan=True):
        """
        :param estimator: estimator can be 'RandomForest', 'SVM'.
        :param remove_nan: remove np.nan values from X
        """
        self.estimator = estimator
        self.remove_nan = remove_nan

    def fit(self, X, y):
        """
        Fit the model.
        :param X: {array-like, sparse matrix, dataframe} of shape (n_samples, n_features)
        :param y: ndarray of shape (n_samples,) Target values.
        :return: self
        """
        if self.estimator == 'RandomForest':
            self.estimator = RandomForestClassifier()
        elif self.estimator == 'SVM':
            self.estimator = SVC()
        else:
            raise ValueError('You chosen an incorrect estimator')

        # Return digit-view of y
        self.classes_, y = np.unique(y, return_inverse=True)

        if self.remove_nan:
            # Find rows having at least 1 np.nan value in its columns
            indexes = ~np.isnan(X).any(axis=1)
            X = X[indexes]
            y = y[indexes]
        else:
            X = SimpleImputer().fit_transform(X)

        return self.estimator.fit(X, y)

    def predict(self, X):
        predicted = self.estimator.predict(X)
        return np.apply_along_axis(lambda k: self.classes_[k], 0, predicted)

    def score(self, X, y, sample_weight=None):
        return f1_score(y, self.predict(X), sample_weight=sample_weight, average='weighted')
