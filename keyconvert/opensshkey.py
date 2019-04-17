# Copyright Anton Semjonov, Licensed under GPL-3.0

from sys import stderr
from keyconvert.buffer import Buffer


class OpenSSHKey:
    """Parse an OpenSSH key from a passed Buffer."""

    def __init__(self, keybuf, verbose=False):

        # cipher and kdf need to be 'none', i.e. the key must not be encrypted
        if keybuf.readString() != b"none":
            raise ValueError("Cipher is not b'none'!")
        if keybuf.readString() != b"none":
            raise ValueError("KDF is not b'none'!")
        if keybuf.readString() != b"":
            raise ValueError("KDF options are not empty!")

        # check that the number of keys is equal to 1
        if keybuf.readUInt32() != 1:
            raise ValueError("More than one key inside!")

        # read and ignore public key
        keybuf.readString()

        # get secretkey blob and check that there is no additional data at the end
        blob = Buffer(keybuf.readString())
        if keybuf.status()["remaining"] != 0:
            raise ValueError("There is data after the secretkey blob!")
        keybuf.close()

        # check that there are two identical uint32's at the beginning
        if blob.readUInt32() != blob.readUInt32():
            raise ValueError("Magic numbers in secretkey blob do not match!")

        # parse key contents
        self.__parseSecretBlob(blob)

        # check for correct padding at the end of the secret
        for i in range(blob.status()["remaining"]):
            if i > 255 or blob.readUInt8() != i + 1:
                raise ValueError("Padding at the end of the secretkey blob is incorrect!")
        blob.close()

        if verbose:
            print("Successfully read %s key (%s)." % (self.type, self.comment))

    def __parseSecretBlob(self, blob):
        """Parse a secretkey blob and set contents."""

        # read key type
        self.type = blob.readString().decode("utf-8")

        # parse curve parameters depending on keytype
        if self.type == "ssh-ed25519":
            self.curve = "ed25519"
            self.public = blob.readString()
            self.secret = blob.readString()

        elif self.type == "ecdsa-sha2-nistp256":
            print("WARNING: ECDSA key support is incomplete and incompatible with tinyssh!", file=stderr)
            # since version 20190101 tinyssh deprecated and removed ecdsa anyway ...
            self.curve = blob.readString().decode("utf-8")
            coordinates = Buffer(blob.readString())
            compression = coordinates.readUInt8()
            if compression != 0x04:
                print("the ecdsa coordinates in compressed form!")
            x = coordinates.readBytes(32)
            y = coordinates.readBytes(32)
            self.secret = x + y
            self.public = blob.readString()

        else:
            raise ValueError("Unknown key type: %s" % self.type)

        # comment
        self.comment = blob.readString().decode("utf-8")

    def json(self, indent=None):
        from base64 import b64encode as base64
        from json import dumps as json

        return json(
            {
                "type": self.type,
                "curve": self.curve,
                "public": base64(self.public).decode("utf-8"),
                "secret": base64(self.secret).decode("utf-8"),
                "comment": self.comment,
            },
            indent=indent,
        )

