#!/usr/bin/env python3

from setuptools import setup, find_packages

setup(
  name = "tinyssh-convert",
  version = "0.0.1",
  author = "Anton Semjonov",
  scripts = ["tinyssh-keyconvert.py"],
  package_dir = { 'keyconvert': 'keyconvert' },
  packages = find_packages(),
)
