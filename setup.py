#!/usr/bin/env python3
# Copyright Anton Semjonov, Licensed under GPL-3.0

from setuptools import setup, find_packages
from keyconvert.package import package

setup(
  name = package['name'],
  version = package['version'],
  author = package['author'],
  author_email = package['author_email'],
  scripts = ["tinyssh-keyconvert"],
  package_dir = { 'keyconvert': 'keyconvert' },
  packages = find_packages(),
  data_files = [ 'package.json' ],
)
