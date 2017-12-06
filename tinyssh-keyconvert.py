#!/usr/bin/env python3

"""Convert armored OpenSSH key to binary TinySSH format."""

from argparse import ArgumentParser

from keyconvert.opensshkey import OpenSSHKey

A = ArgumentParser()
A.add_argument('-k', '--key', help='OpenSSH private key', required=True)
args = A.parse_args()

key = OpenSSHKey(args.key)

print(key.toJSON())
