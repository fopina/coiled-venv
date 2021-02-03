import platform
import os
from pathlib import Path


__platform = platform.system()
ON_MACOS = os.name == 'mac' or __platform == 'Darwin'
ON_WINDOWS = os.name == 'nt' or __platform == 'Windows'
DEFAULT_SHELL = 'cmd' if ON_WINDOWS else 'bash'

# TODO: make this configurable
VENV_DIR = Path.home() / '.virtualenvs'
CONF_DIR = Path.home() / '.coil'
ENV_DB = CONF_DIR / 'mapping.json'


def setup_conf():
    CONF_DIR.mkdir(exist_ok=True)
