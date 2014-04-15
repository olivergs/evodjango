# -*- coding: utf-8 -*-
"""
EVODjango Django extensions for development aid
===============================================

.. module:: pyevo
    :platform: Unix, Windows
    :synopsis: EVODjango Django extensions for development aid
.. moduleauthor:: (C) 2013 Oliver Gutiérrez
"""
# Python imports
import os

from setuptools import setup, find_packages

README = open(os.path.join(os.path.dirname(__file__), 'README.md')).read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='evodjango',
    packages = find_packages(),
    version='0.1',
    description='EVODjango Django extensions for development aid',
    long_description=README,
    license='MIT License',
    author="Oliver Gutiérrez",
    author_email="ogutsua@gmail.com",
    url = 'https://github.com/R3v1L/evodjango',
    keywords = ['evodjango', 'django', 'utility', ],
    classifiers = [],
    # download_url = '',
)