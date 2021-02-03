from . import __description__, __version__
import argparse
import sys
import os
import platform
import json
from pathlib import Path

__platform = platform.system()
ON_MACOS = os.name == 'mac' or __platform == 'Darwin'
ON_WINDOWS = os.name == 'nt' or __platform == 'Windows'

# TODO: make this configurable
VENV_DIR = Path.home() / '.virtualenvs'
CONF_DIR = Path.home() / '.coil'
ENV_DB = CONF_DIR / 'mapping.json'


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


def venv_bin(path):
    d = path / 'bin'
    if d.is_dir():
        return d
    if ON_WINDOWS:
        d = path / 'Scripts'
        if d.is_dir():
            return d
    return None


def is_venv(path):
    return venv_bin(path) is not None


def list_environments():
    for l in VENV_DIR.glob('*'):
        if is_venv(l):
            print(l.name)
    

def env_for_path(path=None):
    if path is None:
        path = Path.cwd()
    return None


def load_env(path):
    print('LOADING')


def setup_conf():
    CONF_DIR.mkdir(exist_ok=True)


class DB(dict):
    def __init__(self, *a, **b):
        super().__init__(self, *b, **b)

    def load(self):
        self.clear()
        try:
            with open(ENV_DB) as f:
                self.update(json.load(f))
        except FileNotFoundError:
            pass

    def dump(self):
        with open(ENV_DB, 'wb') as f:
            json.dump(self, f)


def bind_env(name):
    setup_conf()
    db = DB()
    db['x'] = 1
    db.dump()


def main(args=None):
    args = parseargs(args)
    if args.list:
        return list_environments()
    
    if args.bind:
        env = bind_env(args.bind)
        if env is None:
            print(f'env {args.bind} does not exist. Use -c instead to create it or -l to see the ones available')
            return 1
        load_env(env)

    env = env_for_path()
    if env is None:
        print('No env configured for current directory. Use "-b ENV" to bind an existing one or "-c ENV" to create and bind to a new one')
        return 1
    
    load_env(env)
    # no return needed: exec or Exception


if __name__ == '__main__':
    exit(main())
