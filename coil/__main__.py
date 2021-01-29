from . import __description__, __version__
import argparse
import sys


def parseargs(args):

    parser = argparse.ArgumentParser(
        add_help=False,
        description=__description__,
        usage='%(prog)s [OPTIONS] message...',
    )
    parser.add_argument('-h', '--help', action='help', help=argparse.SUPPRESS)
    parser.add_argument('-s', '--service', action='store', help='use only this service')
    parser.add_argument('--list-services', action='store_true')
    parser.add_argument(
        '-c',
        '--config',
        action='store',
        help='use this configuration file instead of ~/.notifypush',
    )
    parser.add_argument('--version', action='version', version=__version__)
    parser.add_argument('message', metavar='message', nargs='*', help='message')

    return parser.parse_args(args)


def main(args=None):
    print('placeholder')


if __name__ == '__main__':
    main()
