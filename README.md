# tinyssh-keyconvert

Convert OpenSSH ed25519 / ecdsa-nistp256 secret keys to binary format for TinySSH.

**Note**: ecdsa support is incomplete!

## SYNOPSIS

Specify the path to your private key as a positional argument and the script will read, parse,
convert and write the TinySSH keys to the default location in `/etc/tinyssh/sshkeydir`.

```
tinyssh-keyconvert /etc/ssh/ssh_host_ed25519_key
```

## USAGE

Various flags to control the script execution are available:

|    flag     | description                                           |
| :---------: | ----------------------------------------------------- |
|  `--help`   | display usage help                                    |
| `--verbose` | be more verbose, enable tracebacks                    |
|  `--json`   | print a JSON representation of the parsed key         |
| `--dir DIR` | specify output directory `DIR` for the converted keys |
|  `--force`  | force overwriting existing files                      |
| `--dry-run` | do not write converted keys, only parse               |

A complete and up-to-date usage note can be obtained by running `tinyssh-keyconvert --help`.

The converted keys are named `ed25519.pk`/`.ed25519.sk` and `nistp256ecdsa.pk`/`.nistp256ecdsa.sk`
respectively.

### Usage with ECDSA-SHA2-NISTP256

This keytype is not fully supported yet! Right now it simply writes the public and secret parts to
files without parsing or unwrapping the keys any further. `tinysshd-printkeys` does not complain but
the hostkey fingerprints differ!

## INSTALLATION

Use [`pip`](https://pip.pypa.io/en/stable/installing/) to install this package directly from GitHub:

```
pip install git+https://github.com/ansemjo/tinyssh-convert.py
```

Or install a tagged release from the
[Releases](https://github.com/ansemjo/tinyssh-convert.py/releases) page:

```
pip install https://github.com/ansemjo/tinyssh-convert.py/archive/v0.3.0.zip
```

## LICENSE

Copyright (c) 2019 Anton Semjonov, licensed under the [GNU General Public License 3.0](LICENSE)
