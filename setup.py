#!/usr/bin/env python3
# Copyright Anton Semjonov, Licensed under GPL-3.0

from subprocess import check_output as cmd
from setuptools import setup, find_packages

setup(
    name="tinyssh-keyconvert",
    description="Convert OpenSSH ed5519/ecdsa-nistp256 secretkeys to binary format for TinySSH.",
    keywords="openssh tiyssh privatekey key converter",
    version=cmd(["sh", "./version.sh", "describe"]).strip().decode(),
    license="GPL-3.0",
    author="Anton Semjonov",
    author_email="anton@semjonov.de",
    url="https://github.com/ansemjo/tinyssh-keyconvert",
    scripts=["tinyssh-keyconvert"],
    packages=find_packages(),
    python_requires=">3",
)
