# tinyssh-keyconvert

Convert OpenSSH ECDSA-nistp256/ED25519 secretkeys to binary format for
TinySSH.

## Usage

You can either use the file `./tinyssh-keyconvert` directly if you have a
recent copy of [Python](https://www.python.org/) installed or run the
Installation steps first.

A complete and up-to-date usage note can be obtained by running
`./tinyssh-keyconvert --help`:

```
usage: tinyssh-keyconvert [-h] [-v] -k KEY [-d DIR] [-f] [-j]

Convert OpenSSH ECDSA-nistp256/ED25519 secretkeys to binary format for
TinySSH.

optional arguments:
  -h, --help         show this help message and exit
  -v, --verbose      be verbose

input:
  -k KEY, --key KEY  openssh secret key

output:
  -d DIR, --dir DIR  write key files to destination directory
  -f, --force        overwrite existing files
  -j, --json         output a json representation to stdout
```

### Usage with ECDSA-SHA2-NISTP256

This keytype is not fully supported yet! Right now it simply writes the public
and secret parts to files without parsing or unwrapping the keys any further.
`tinysshd-printkeys` does not complain but the hostkey fingerprints differ!

## Installation

Use the included `./setup.py` script to install this program. It may require
you to install the [`setuptools`](https://pypi.python.org/pypi/setuptools/)
package first.

* install system-wide: `./setup.py install` (may require elevated permissions)
* install for your user: `./setup.py install --user`

The latter installs the executable under `~/.local/bin/` by default. Make sure
you have that directory in your `PATH` variable.

## License

Copyright 2017 Anton Semjonov

```
This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License (Version 3.0)
as published by the Free Software Foundation.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
```