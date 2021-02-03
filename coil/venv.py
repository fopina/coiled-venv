from pathlib import Path

from . import config as C, db, shell


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
    print('LOADING', path)
    bd = bindir(path)
    if bd is None:
        raise Exception('how did you get here??')
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
        raise Exception(f'{path} is already bound to {path_str}')
    dbi[path_str] = name
    dbi.dump()
    return venv_path


def for_path(path=None):
    if path is None:
        path = Path.cwd()
    else:
        path = path.absolute()
    root = Path(path.root)
    while path != root:
        r = db.DB().get(str(path))
        if r is not None:
            return C.VENV_DIR / r
        path = path.parent
    return None