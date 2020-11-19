from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import GridSearchCV
import pandas as pd
import pickle


class Model:
    def __init__(self, data: pd.DataFrame):
        if not isinstance(data, pd.DataFrame):
            raise TypeError("The data isn't instance of pd.DataFrame")
        self._data = data
        self.X = data.drop('author', axis=1).values
        self.y = data['author'].values
        self.model = None

    def fit(self, scaling=True):
        """
        Fit the model.
        :param scaling: to scale the features
        """
        X = self.X
        if scaling:
            X = StandardScaler().fit_transform(self.X)
        y = LabelEncoder().fit_transform(self.y)

        param_grid = [
            {'n_estimators': [50, 100, 200], 'max_depth': [2, 6, 9], 'min_samples_leaf': [1, 2, 3]}
        ]

        print('Begin searching the best hyper parameters of the model...')
        clf = GridSearchCV(RandomForestClassifier(), param_grid, n_jobs=-1, verbose=1, cv=5)
        clf.fit(X, y)
        self.model = clf.best_estimator_
        print('Best score of the model: ', clf.best_score_)
        print('Best estimator: ', clf.best_estimator_)

    def save(self, name: str):
        """
        Save the model into the .pickle file.
        :param name: the name of the file
        """
        with open(name, 'wb') as file:
            pickle.dump(self.model, file)