#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function
import os
from setuptools import setup, find_packages
import sys

from coil import __program__, __version__, __description__

README = open('README.md').read()

# allow setup.py to be run from any path
os.chdir(os.path.dirname(os.path.abspath(__file__)))

setup(
    name=__program__,
    version=__version__,
    license='MIT',
    description=__description__,
    long_description=README,
    url='https://github.com/fopina/coiled-venv',
    download_url='https://github.com/fopina/coiled-venv/tarball/v%s' % __version__,
    author='Filipe Pina',
    author_email='fopina@skmobi.com',
    packages=find_packages(),
    entry_points={'console_scripts': ['coil=coil.__main__:main']},
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
    keywords=['productivity', 'virtual env', 'cleanup', 'cli'],
)
