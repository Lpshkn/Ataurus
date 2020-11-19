import sys
import configurator as cfg
from preparing.preparator import Preparator
from features.extractor import FeaturesExtractor
from ml.model import Model


def main():
    configurator = cfg.Configurator(sys.argv[1:])

    if configurator.command == 'info':
        pass
    elif configurator.command == 'train':
        preparator = Preparator(configurator.input_data)
        extractor = FeaturesExtractor(preparator)
        extractor.fit()
        print('FEATURES:\n', extractor.features)
        model = Model(extractor.features)
        model.fit()
        model.save(configurator.output_file)
    elif configurator.command == 'predict':
        pass


if __name__ == '__main__':
    main()
