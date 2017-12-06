#!/usr/bin/env python3

"""Convert armored OpenSSH key to binary TinySSH format."""

from argparse import ArgumentParser

from keyconvert.readkey import readkey
from keyconvert.seckey import SecKey

A = ArgumentParser()
A.add_argument('-k', '--key', help='OpenSSH private key', required=True)
args = A.parse_args()

key = SecKey(readkey(args.key))

print(key.toJSON())
