from pathlib import Path
import venv as pyvenv
import random
import shutil
import subprocess

from . import config as C, db, shell


class VenvError(Exception):
    """
    errors managing virtualenvs
    """


def bindir(path):
    d = path / 'bin'
    if d.is_dir():
        return d
    if C.ON_WINDOWS:
        d = path / 'Scripts'
        if d.is_dir():
            return d
    return None


def check(path):
    return bindir(path) is not None


def list_available():
    for l in C.VENV_DIR.glob('*'):
        if check(l):
            yield l.name


def load(path):
    print(f'Loading {path}...')
    bd = bindir(path)
    if bd is None:
        raise VenvError('how did you get here??')
    l, p = shell.get_shell()
    l(bd, p)


def bind(name, path=None):
    if path is None:
        path = Path.cwd()
    C.setup_conf()
    venv_path = C.VENV_DIR / name
    dbi = db.DB()
    path_str = str(path)
    if path_str in dbi:
        raise VenvError(f'{path} is already bound to {path_str}')
    dbi[path_str] = name
    dbi.dump()
    return venv_path


def unbind(path=None):
    env, ppath = for_path_helper(path)
    if env is None:
        raise VenvError(f'{path} is NOT bound to any env')
    dbi = db.DB()
    del dbi[str(ppath)]
    dbi.dump()


def new(name=None):
    if name is None:
        # generate random one
        name = f'auto_{int(random.random()*16777215):x}'
    venv_path = C.VENV_DIR / name
    pyvenv.create(venv_path, with_pip=True)
    return name


def shed(name):
    venv_path = C.VENV_DIR / name
    if not venv_path.exists():
        raise VenvError(f'{name} does not exist')
    shutil.rmtree(venv_path)


def for_path_helper(path=None):
    if path is None:
        path = Path.cwd()
    else:
        path = path.absolute()
    root = Path(path.root)
    while path != root:
        r = db.DB().get(str(path))
        if r is not None:
            return C.VENV_DIR / r, path
        path = path.parent
    return None, path


def for_path(path=None):
    return for_path_helper(path)[0]
