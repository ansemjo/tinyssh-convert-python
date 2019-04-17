# Copyright Anton Semjonov, Licensed under GPL-3.0

from struct import unpack


def unpack_uint32(by):
    """Parse four big-endian bytes as 32 bit unsigned integer."""
    return unpack(">I", by)[0]


def unpack_uint8(by):
    """Parse one byte as unsigned char."""
    return unpack(">B", by)[0]


class Buffer:
    """Buffer for sequential reading."""

    def __init__(self, buf):
        self.buf = buf
        self.offset = 0

    def status(self):
        """Return positional status (current, length, remaining)."""
        o = self.offset
        l = len(self.buf)
        return {"current": o, "length": l, "remaining": l - o}

    def close(self):
        del self.buf

    def readBytes(self, n):
        """Read n bytes and adjust offset for next read."""
        s = self.status()
        if s["remaining"] < n:
            raise ValueError(
                "Cannot read bytes from buffer, offset too large! (%d + %d > %d)"
                % (s["current"], n, s["length"])
            )
        self.offset += n
        return self.buf[self.offset - n : self.offset]

    def readUInt8(self):
        """Read next byte as unsigned char."""
        return unpack_uint8(self.readBytes(1))

    def readUInt32(self):
        """Read four bytes as unsigned integer."""
        return unpack_uint32(self.readBytes(4))

    def readString(self):
        """Read the next string defined by: [uint32 length, string]"""
        return self.readBytes(self.readUInt32())

