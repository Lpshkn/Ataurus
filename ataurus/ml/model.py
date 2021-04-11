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
        """
        Predict targets.
        :param X: {array-like, sparse matrix, dataframe} of shape (n_samples, n_features)
        :return: predicted targets
        """
        if not self.estimator:
            raise ValueError("The model wasn't fitted, so it can't predict labels")

        X = StandardScaler().fit_transform(X)
        return self.estimator.predict(X)

    def save(self, name: str):
        """
        Save the model into the .pickle file.
        :param name: the name of the file
        """
        if not self.estimator:
            raise ValueError("The model wasn't fitted, so it can't be saved")

        with open(name, 'wb') as file:
            pickle.dump(self, file)

    def info(self):
        if not self.estimator:
            raise ValueError("The model wasn't fitted, so it hasn't any information")

        print('Estimator:', self.estimator.__class__.__name__)
        print('Best score:', self.best_score)
        print('Parameters:')
        for param, value in self.best_params.items():
            print(f'\t{param}:', value)
