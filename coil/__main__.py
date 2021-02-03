from . import __description__, __version__
import argparse
import sys
import os
import platform
import json
from pathlib import Path

from .config import ON_WINDOWS, VENV_DIR, CONF_DIR, ENV_DB
from . import db, venv


def parseargs(args):
    parser = argparse.ArgumentParser(
        add_help=False,
        description=__description__,
        usage='%(prog)s [OPTIONS] ...',
    )
    parser.add_argument('-h', '--help', action='help', help=argparse.SUPPRESS)
    parser.add_argument('-l', '--list', action='store_true', help='list available venvs')
    parser.add_argument('-b', '--bind', type=str, metavar='ENV', help='bind venv to current path')
    parser.add_argument('--version', action='version', version=__version__)

    return parser.parse_args(args)



class CommandError(Exception):
    pass


def main(args=None):
    args = parseargs(args)
    if args.list:
        for _e in venv.list_available():
            print(_e)
        return 0

    if args.bind:
        env = venv.bind(args.bind)
        if env is None:
            print(f'env {args.bind} does not exist. Use -c instead to create it or -l to see the ones available')
            return 1
        venv.load(env)

    env = venv.for_path()
    if env is None:
        print('No env configured for current directory. Use "-b ENV" to bind an existing one or "-c ENV" to create and bind to a new one')
        return 1
    
    venv.load(env)


if __name__ == '__main__':
    exit(main())
