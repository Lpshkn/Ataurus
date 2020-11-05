import sys
import configurator as cfg
from preparing.preparator import Preparator


def main():
    try:
        configurator = cfg.Configurator(sys.argv[1:])
        preparator = Preparator(configurator.data)

        tokens = preparator.tokens()
        print("Tokens: ", tokens)
        sentences = preparator.sentences()
        print("Sentences: ", sentences)
    except Exception as e:
        print('Error:', e, file=sys.stderr)


if __name__ == '__main__':
    main()
