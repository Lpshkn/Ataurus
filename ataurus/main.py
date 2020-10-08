import sys
import configurator as cfg


def main():
    try:
        configurator = cfg.Configurator(sys.argv[1:])
        configurator.data
    except Exception as e:
        print('Error:', e, file=sys.stderr)

if __name__ == '__main__':
    main()
