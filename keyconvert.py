"""Convert armored OpenSSH key to binary TinySSH format."""

from readkey import readkey
from key import SecKey
from json import dumps as json

key = SecKey(readkey('./testkey'))

print(key.toJSON())