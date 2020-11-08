import sys
import configurator as cfg
from preparing.preparator import Preparator


def main():
    configurator = cfg.Configurator(sys.argv[1:])
    preparator = Preparator(configurator.data)

    tokens = preparator.tokens()
    for _tokens in tokens:
        print("Tokens:\n", "\n".join(_tokens))
    print('-'*100)
    sentences = preparator.sentences()
    for _sentences in sentences:
        print("Sentences:\n", "\n".join(_sentences))


if __name__ == '__main__':
    main()
