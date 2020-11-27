import sys
import configurator as cfg
from preparing.preparator import Preparator
from features.extractor import FeaturesExtractor
from ml.model import Model


def main():
    configurator = cfg.Configurator(sys.argv[1:])

    if configurator.command == 'info':
        model = configurator.model
        model.info()

    elif configurator.command == 'train':
        preparator = Preparator().fit(configurator.input_data)
        extractor = FeaturesExtractor().fit(preparator.tokens(), preparator.sentences(), preparator.authors)
        print('FEATURES:\n', extractor.features)

        model = Model()
        X = extractor.features.drop('author', axis=1)
        y = extractor.features['author']
        model.fit(X, y)
        model.save(configurator.output_file)

    elif configurator.command == 'predict':
        preparator = Preparator().fit(configurator.input_data)
        extractor = FeaturesExtractor().fit(preparator.tokens(), preparator.sentences(), preparator.authors)

        model = configurator.model
        X = extractor.features.drop('author', axis=1)
        print('Predictions:', model.predict(X))


if __name__ == '__main__':
    main()
