#!/usr/bin/env python

import os
import re
import sys

from codecs import open

from setuptools import setup


if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    sys.exit()

packages = [
    'inkah',
]

requires = []

with open('inkah/__init__.py', 'r') as fd:
    version = re.search(r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]',
                        fd.read(), re.MULTILINE).group(1)

if not version:
    raise RuntimeError('Cannot find version information')

# with open('README.md', 'r', 'utf-8') as f:
#     readme = f.read()

setup(
    name='inkah',
    version=version,
    description='Inkah utilities for Python.',
    # long_description=readme,
    author='Mike Leonard',
    author_email='mike.r.leonard@gmail.com',
    url='https://github.com/mleonard87/inkah-python',
    packages=packages,
    package_data={'': ['LICENSE']},
    package_dir={'inkah': 'inkah'},
    include_package_data=True,
    install_requires=requires,
    license='MIT',
    zip_safe=False,
    classifiers=(
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ),
)
