#!/usr/bin/env python3

from setuptools import setup, find_packages

setup(
    name='huh-computer-music',
    version='0.1',
    description='A tiny computer music library powered by NumPy',
    long_description=open('README.md', 'r').read(),
    license='MIT',
    author='Jason Doar & Alex Rosengarten',
    maintainer_email='alxrsngrtn@gmail.com',
    platforms=['darwin', 'linux'],
    url='https://github.com/alxrsngrtn/huh-computer-music',
    install_requires=[x.strip() for x in open('requirements.txt', 'r').readlines()],
    extras_require={
        'dev': [x.strip() for x in open('dev_requirements.txt', 'r').readlines()]
    },
    packages=find_packages(),
    scripts=['hcm/bish']
)
