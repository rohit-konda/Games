#!/usr/bin/env python

from setuptools import setup, find_packages

setup(name='games',
      version='1.0',
      description='A game-theoretic python package',
      URL='https://github.com/rohit-konda/Games.git',
      author='Rohit Konda',
      author_email='rkonda@ucsb.edu',
      license='MIT',
      packages=find_packages(include=["games*"]),
      install_requires=['numpy'],
      classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.7',
      ],
      zip_safe=False)
