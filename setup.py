#! /usr/bin/env python3

from setuptools import setup, find_packages

with open('requirements.txt') as fd:
    strip_comment = lambda s: s.split('#', 1)[0].strip()
    requires = [strip_comment(line) for line in fd.readlines() if strip_comment(line)]

setup(
    name='burje_instrument',
    version='0.1.0',
    description='',
    url='',
    install_requires=requires,
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    license='Proprietary',
    author="Tide KYC Decisioning team",
)