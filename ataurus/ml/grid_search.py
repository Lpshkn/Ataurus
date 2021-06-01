"""
The default grid params for the GridSearchCV of sklearn.model_selection.
There are the main parameters corresponding recommended features and hyper parameters of models.
You may specify your values, just look at the official documentation of Scikit-Learn for a specific class.
"""
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC


PARAM_GRID_DEFAULT = [
    {
        "combine__avg_words": [True],
        "combine__avg_sentences": [True],
        "combine__pos_distribution": [True],
        "combine__foreign_words_ratio": [True],
        "combine__lexicon": [True],
        "combine__punctuation_distribution": [True],

        "model__estimator": [RandomForestClassifier()],
        "model__estimator__n_estimators": [100],
        "model__estimator__criterion": ["gini", "entropy"],
        "model__estimator__max_depth": [2, 5, 10, None],
        "model__estimator__min_samples_split": [2, 6, 10],
        "model__estimator__min_samples_leaf": [2, 5, 10],
        "model__estimator__max_leaf_nodes": [3, 5, 10, None]
    },
    {
        "combine__avg_words": [True],
        "combine__avg_sentences": [True],
        "combine__pos_distribution": [True],
        "combine__foreign_words_ratio": [True],
        "combine__lexicon": [True],
        "combine__punctuation_distribution": [True],

        "model__estimator": [SVC()],
        "model__estimator__C": [0.2, 0.5, 1],
        "model__estimator__kernel": ["linear", "poly", "rbf"],
        "model__estimator__degree": [2, 3, 4],
        "model__estimator__gamma": [0.1, 0.5, 1]
    }
]
