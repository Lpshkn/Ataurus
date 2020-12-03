import sys
import ataurus.configurator.configurator as cfg
import pandas as pd
from ataurus.preparing.preparator import Preparator
from ataurus.features.extractor import FeaturesExtractor
from ataurus.ml.model import Model


def main():
    configurator = cfg.Configurator(sys.argv[1:])

    if configurator.command == 'info':
        model = configurator.model
        model.info()
    else:
        input_obj = configurator.input

        if isinstance(input_obj, FeaturesExtractor):
            extractor = input_obj
        elif isinstance(input_obj, pd.DataFrame):
            preparator = Preparator().fit(input_obj)
            extractor = FeaturesExtractor().fit(preparator.tokens(), preparator.sentences(), preparator.authors)
            configurator.to_cache(extractor)

        if configurator.command == 'train':
            print('FEATURES:\n', extractor.features)
            model = Model()
            model.fit(extractor.X, extractor.y)
            model.save(configurator.output_file)
        elif configurator.command == 'predict':
            model = configurator.model
            print('Predictions:', model.predict(extractor.X))


if __name__ == '__main__':
    main()
