import signal
import os
from pathlib import Path
import subprocess

from . import config as C

def zsh_shell(exe_dir, shell_path):
    rcfile = exe_dir / '.coil.zsh' / '.zshrc'
    rcfile.parent.mkdir(exist_ok=True)
    with open(rcfile, 'w') as f:
        f.write(f'''\
. ~/.zshrc
. {exe_dir / 'activate'}
''')
    os.environ['ZDOTDIR'] = str(rcfile.parent)
    os.execlp(shell_path or 'zsh', '-i')


def bash_shell(exe_dir, shell_path):
    pass


def get_shell():
    shell_path = os.environ.get('SHELL')
    if shell_path:
        shell_path = Path(shell_path)
        shell_name = shell_path.name
    else:
        shell_name = C.DEFAULT_SHELL
    return SHELL_COMMANDS.get(shell_name), shell_path


# SHELL_COMMANDS = {
#     'cmd': cmd_shell,
#     'powershell': ps_shell,
#     'ps': ps_shell,
#     'bash': bash_shell,
#     'fish': fish_shell,
#     'zsh': zsh_shell,
#     'xonsh': xonsh_shell,
#     'tcsh': tcsh_shell,
#     'csh': csh_shell,
# }


SHELL_COMMANDS = {
    'zsh': zsh_shell,
    'bash': bash_shell,
}