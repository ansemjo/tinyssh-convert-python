# Copyright Anton Semjonov, Licensed under GPL-3.0

from base64 import b64decode
from tinyssh_keyconvert.buffer import Buffer
from os.path import realpath
from os import umask


def read_openssh_v1_key(keyfile):
    """Read OpenSSH-Key-V1 compatible file and return a Buffer of its contents."""

    armor = keyfile.read().split("\n")
    keyfile.close()
    string = ""

    # begin, end and magic markers
    BEGINTAG = "-----BEGIN OPENSSH PRIVATE KEY-----"
    ENDTAG = "-----END OPENSSH PRIVATE KEY-----"
    OPENSSH_MAGIC = b"openssh-key-v1\x00"

    for index, line in enumerate(armor):

        if index == 0:
            # first line must have the begin tag
            if line != BEGINTAG:
                raise ValueError("expected OPENSSH PRIVATE KEY begin tag")
            else:
                continue

        if index == (len(armor) - 1) and line != ENDTAG:
            # reached last line with no end tag
            raise ValueError("unexpected end of file, no end tag")

        if line == ENDTAG:
            # reached end tag, end loop
            break

        # default action: concatenate base64 string
        string += line

    bytestring = b64decode(string)
    key = Buffer(bytestring)

    if key.readBytes(len(OPENSSH_MAGIC)) == OPENSSH_MAGIC:
        return key
    else:
        raise ValueError("Not an OpenSSH V1 key!")


# filename mapping of tinyssh keys
TINYSSH_FILENAME = {
    "ssh-ed25519": {
      "public": "ed25519.pk",
      "secret": ".ed25519.sk"
    },
    "ecdsa-sha2-nistp256": {
      "public": "nistp256ecdsa.pk",
      "secret": ".nistp256ecdsa.sk"
    },
}

# default tinyssh key directory
TINYSSH_KEYDIR = "/etc/tinyssh/sshkeydir"


def write_tinyssh_keys(key, force=False, directory=TINYSSH_KEYDIR, verbose=False):
    """Write a converted key hash with private and public parts to files in directory."""
    for keypart in ("public", "secret"):
        if keypart == "secret":
          oldumask = umask(0o077)
        path = realpath("%s/%s" % (directory, TINYSSH_FILENAME[key.type][keypart]))
        with open(path, mode="wb" if force else "xb") as outfile:
            if verbose:
                print("Writing %s/%s to %s" % (key.type, keypart, path))
            outfile.write(getattr(key, keypart))
        if keypart == "secret":
          umask(oldumask)

