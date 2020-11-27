from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import GridSearchCV
import pandas as pd
import pickle


class Model:
    def __init__(self):
        self.estimator = None
        self.best_score = None
        self.best_params = None

    def fit(self, X, y):
        """
        Fit the model.
        :param X: {array-like, sparse matrix, dataframe} of shape (n_samples, n_features)
        :param y: ndarray of shape (n_samples,) Target values.
        :return: self
        """
        param_grid = {
            'n_estimators': [50, 100, 200, 300],
            'max_depth': [2, 4, 6, 8, 9],
            'min_samples_leaf': [1, 2, 3, 4],
            'criterion': ['gini', 'entropy'],
            'max_features': ['sqrt', 'log2']
        }

        print('Begin searching the best hyper parameters of the model...')
        clf = GridSearchCV(RandomForestClassifier(), param_grid, n_jobs=-1, verbose=1, cv=5)
        clf.fit(X, y)
        self.estimator = clf.best_estimator_
        self.best_score = clf.best_score_
        self.best_params = clf.best_params_
        print('Best score of the model: ', clf.best_score_)
        print('Best estimator: ', clf.best_estimator_)
        print('Best parameters: ')
        for param, value in self.best_params.items():
            print(f'\t{param}:', value)

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
