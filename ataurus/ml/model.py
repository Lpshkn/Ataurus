from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.base import BaseEstimator, ClassifierMixin
from sklearn.metrics import f1_score


class Model(BaseEstimator, ClassifierMixin):
    def __init__(self, estimator):
        """
        :param estimator: estimator can be 'RandomForest', 'SVM'.
        """
        self.estimator = estimator

    def fit(self, X, y=None):
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

        if isinstance(X, tuple):
            train, targets = X
        else:
            if y is None:
                raise ValueError('y is None')
            train = X
            targets = y

        return self.estimator.fit(train, targets)

    def predict(self, X):
        return self.estimator.predict(X)

    def score(self, X, y, sample_weight=None):
        return f1_score(y, self.predict(X), sample_weight=sample_weight)
