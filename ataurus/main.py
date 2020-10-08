import sys
import configurator as cfg
from preparing.preparator import Preparator


def main():
    try:
        configurator = cfg.Configurator(sys.argv[1:])
    except Exception as e:
        print('Error:', e, file=sys.stderr)


if __name__ == '__main__':
    main()
