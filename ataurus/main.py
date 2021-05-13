import sys
import ataurus.configurator.configurator as cfg
import numpy as np
from ataurus.preparing.preprocessor import Preprocessor
from ataurus.features.extractor import FeaturesExtractor
from ataurus.database.client import Database
from ataurus.ml.model import Model
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import GridSearchCV, RandomizedSearchCV
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC


def main():
    database = Database.connect(['localhost:9200'])
    authors, texts = database.get_authors_texts('articles_5ath', 'author_nickname', 'text')
    preprocessor = Preprocessor(texts)

    texts = np.array(preprocessor.texts(), dtype=object)
    tokens = np.array(preprocessor.tokens(), dtype=object)
    sentences = np.array(preprocessor.sentences(), dtype=object)
    X = np.c_[texts, tokens, sentences]
    y = np.array(authors).ravel()

    pipeline = Pipeline([
        ('extracting', FeaturesExtractor()),
        ('scaler', StandardScaler()),
        ('model', Model())
    ])

    param_grid = [
        {
            # Hyper-parameters of the RandomForest
            'model__estimator': [RandomForestClassifier()],
            'model__estimator__n_estimators': [50, 100, 150, 200],
            'model__estimator__criterion': ['gini', 'entropy'],
            'model__estimator__max_depth': [2, 4, 6, 8, 10],
            'model__estimator__min_samples_split': [2, 3, 4, 5],
            'model__estimator__min_samples_leaf': [1, 2, 5, 10]},
        {
            # Hyper-parameters of the SVM
            'model__estimator': [SVC()],
            'model__estimator__C': [1, 5, 10, 20, 30],
            'model__estimator__kernel': ['linear', 'poly', 'rbf', 'sigmoid'],
            'model__estimator__degree': [2, 3, 4]
        }
    ]

    random_search = RandomizedSearchCV(pipeline, param_grid, n_iter=20, n_jobs=-1, cv=3)
    random_search.fit(X, y)
    print(random_search.best_estimator_)
    print(random_search.best_params_)
    print(random_search.best_score_)


if __name__ == '__main__':
    main()
