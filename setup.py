# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

try:
    long_description = open("README.rst").read()
except IOError:
    long_description = ""

setup(
    name="polyswarm-artifact",
    version="0.1.0",
    description="Library containing artifact type enums and functions",
    license="MIT",
    author="PolySwarm Developers",
    packages=find_packages('src'),
    package_dir={'': 'src'},
    install_requires=[],
    long_description=long_description,
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.6",
    ]
)
