#!/usr/bin/env python3

"""Convert armored OpenSSH key to binary TinySSH format."""

from readkey import readkey
from key import SecKey

from argparse import ArgumentParser

A = ArgumentParser()
A.add_argument('-k', '--key', help='OpenSSH private key', required=True)
args = A.parse_args()

key = SecKey(readkey(args.key))

print(key.toJSON())