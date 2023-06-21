from . import __description__, __version__
import argparse
import sys
from collections import defaultdict
from pathlib import Path

from . import venv, db


def parseargs(args):
    parser = argparse.ArgumentParser(
        add_help=False,
        description=__description__,
        usage='%(prog)s [OPTIONS] ...',
    )
    parser.add_argument('-h', '--help', action='help', help=argparse.SUPPRESS)
    parser.add_argument('-l', '--list', action='store_true', help='list available venvs')
    parser.add_argument('-b', '--bind', type=str, metavar='ENV', help='bind venv to current path')
    parser.add_argument('-u', '--unbind', action='store_true', help='unbind venv from current path')
    parser.add_argument('-c', '--create', type=str, metavar='ENV', help='create new venv and bind it to current path')
    parser.add_argument(
        '-a', '--auto', action='store_true', help='create new venv (random name) and bind it to current path'
    )
    parser.add_argument('-s', '--shed', type=str, nargs='+', help='remove these virtualenvs')
    parser.add_argument('--fix', action='store_true', help='fix broken python binaries in virtualenv')
    parser.add_argument('--cleanup', action='store_true', help='shed venvs that are not bound to any path')
    parser.add_argument('--version', action='version', version=__version__)

    return parser.parse_args(args)


def main_wrapped(args=None):
    args = parseargs(args)
    if args.list:
        rev_db = defaultdict(set)
        for k, v in db.DB().items():
            if Path(k).exists():
                rev_db[v].add(k)
        for _e in venv.list_available():
            if rev_db.get(_e):
                print(f'{_e} (used in {", ".join(rev_db[_e])})')
            else:
                print(_e)
        return 0

    if args.cleanup:
        dbi = db.DB()
        _keys = list(dbi.keys())
        for k in _keys:
            if not Path(k).exists():
                del dbi[k]
        dbi.dump()

        rev_db = defaultdict(set)
        for k, v in dbi.items():
            if Path(k).exists():
                rev_db[v].add(k)
        for _e in venv.list_available():
            if not rev_db.get(_e):
                print(f'Shedding {_e}...')
                venv.shed(_e)
        return 0

    if args.unbind:
        venv.unbind()
        return

    if args.shed:
        for v in args.shed:
            print(f'Shedding {v}')
            venv.shed(v)
        return

    if args.fix:
        for _e in venv.list_available():
            r = venv.fix_broken(_e)
            if r is not False:
                print(f'Fixed {_e}')
        return

    if args.bind:
        env = venv.bind(args.bind)
        if env is None:
            print(f'env {args.bind} does not exist. Use -c create it or -l to see the ones available')
            return 1
    elif args.create:
        venv.new(name=args.create)
        env = venv.bind(args.create)
    elif args.auto:
        env_name = venv.new()
        env = venv.bind(env_name)
    else:
        env = venv.for_path()
        if env is None:
            print(
                'No env configured for current directory. Use "-b ENV" to bind an existing one or "-c ENV" to create and bind to a new one'
            )
            return 1

    venv.load(env)


def main(args=None):
    try:
        main_wrapped(args=args)
    except venv.VenvError as e:
        print(f'ERROR: {e}', file=sys.stderr)
        return 1


if __name__ == '__main__':
    exit(main() or 0)
