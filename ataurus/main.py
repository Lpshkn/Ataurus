import sys
import asyncio
import pandas as pd
import console_handle.console_handler as cfg
import numpy as np
from preparing.preprocessor import Preprocessor
from features.extract import FeaturesExtractor
from features.combine import FeaturesCombiner
from ml.model import Model
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import GridSearchCV
from serialize.model import serialize_model
from serialize.features import serialize_features
from ml.grid_search import PARAM_GRID_DEFAULT
from data_parse.habr import HabrParser
from database.client import Database


async def main():
    console_handler = cfg.ConsoleHandler(sys.argv[1:])

    if console_handler.mode == 'parse':
        database = Database.connect([f'{console_handler.host}:{console_handler.port}'])
        parser = HabrParser(database=database, concurrent=20)
        dataframe = await parser.parse_by_authors(authors=console_handler.authors, max_count=console_handler.max_count,
                                                  save_to=console_handler.output)
        database.upload_dataframe(index=console_handler.index, dataframe=dataframe, verbose=True)
    else:
        input_data = console_handler.input
        if type(input_data) == tuple:
            if type(input_data[0]) == pd.DataFrame:
                X, y = input_data

                titles = X['titles']
                links = X['links']
            else:
                texts, authors, titles, links = input_data

                titles = np.array(titles, dtype=object)
                links = np.array(links, dtype=object)

                # Extract lists of texts, tokens and sentences
                preprocessor = Preprocessor(texts, authors)
                texts = preprocessor.texts()
                tokens = preprocessor.tokens()
                sentences = preprocessor.sentences()
                authors = preprocessor.authors
                X = np.c_[texts, tokens, sentences]
                y = np.array(authors).ravel()

                # Extract features from texts, tokens and sentences
                extractor = FeaturesExtractor(n_jobs=-1)
                X = extractor.fit_transform(X)
                # Serialize extracted features if it's necessary
                if console_handler.features_path:
                    X['titles'] = titles
                    X['links'] = links
                    serialize_features(X, console_handler.features_path, authors=y)

            # Remove null rows from texts and authors lists
            notnull_indexes = X.notnull().all(axis=1)
            X = X[notnull_indexes]
            y = y[notnull_indexes]
            titles = titles[notnull_indexes]
            links = links[notnull_indexes]
        else:
            X = input_data
            # Remove null rows from texts and authors lists
            notnull_indexes = X.notnull().all(axis=1)
            X = X[notnull_indexes]
            titles = X['titles']
            links = X['links']

        if console_handler.mode == 'train':
            pipeline = Pipeline([
                ('combine', FeaturesCombiner()),
                ('scaler', StandardScaler()),
                ('model', Model())
            ])

            # Run a grid search for searching the best hyper parameters for a model
            param_grid = console_handler.train_config if console_handler.train_config else PARAM_GRID_DEFAULT
            grid_search = GridSearchCV(pipeline, param_grid, n_jobs=-1, cv=5, verbose=1, scoring='f1_weighted')
            grid_search.fit(X, y)

            print("Best score:", grid_search.best_score_)
            print('Best params:', grid_search.best_params_)

            # Serialize the model if it's necessary
            if console_handler.output:
                serialize_model(grid_search.best_estimator_, console_handler.output)

        elif console_handler.mode == 'predict':
            model = console_handler.model
            if console_handler.output:
                with open(console_handler.output, 'w') as file:
                    for title, link, author in zip(titles, links, model.predict(X)):
                        print(author.ljust(20), title.ljust(100), link.ljust(100), file=file)
            else:
                print('Predictions'.center(50, '-'))
                for title, link, author in zip(titles, links, model.predict(X)):
                    print(author.ljust(20), title.ljust(100), link.ljust(100))


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
