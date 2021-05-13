import sys
import ataurus.configurator.configurator as cfg
import numpy as np
from ataurus.preparing.preprocessor import Preprocessor
from ataurus.features.extractor import FeaturesExtractor
from ataurus.database.client import Database
from ataurus.ml.model import Model
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.model_selection import GridSearchCV


def main():
    # configurator = cfg.Configurator(sys.argv[1:])
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
        {'extracting__avg_words': [True],
         'extracting__avg_sentences': [True, False],
         'extracting__pos_distribution': [True, False],
#         'extracting__foreign_words_ratio': [True, False],
         'extracting__vocabulary_richness': [True, False],
#         'extracting__punctuation_distribution': [True, False],
         'model__remove_nan': [True, False],
         'model__estimator': ['RandomForest', 'SVM']}
    ]
    texts = np.array(preprocessor.texts(), dtype=object)
    tokens = np.array(preprocessor.tokens(), dtype=object)
    sentences = np.array(preprocessor.sentences(), dtype=object)
    X = np.c_[texts, tokens, sentences]

    grid_search = GridSearchCV(pipeline, param_grid, n_jobs=-1, cv=2)

    #grid_search.fit(np.c_[texts, np.full(len(texts), None), np.full(len(texts), None)], np.array(authors).ravel())
    grid_search.fit(X, np.array(authors).ravel())
    grid_search

#    if configurator.command == 'train':
#        pass
#    elif configurator.command == 'predict':
#        pass


if __name__ == '__main__':
    main()
