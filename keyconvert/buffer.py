from struct import unpack

def uint32(by):
  """Parse four BE bytes as unsigned integer."""
  return unpack('>I', by)[0]

def uint8(by):
  """Parse one byte as unsigned char"""
  return unpack('>B', by)[0]


class Buffer:
  """Buffer for sequential reading."""

  def __init__(self, buf):
    self.buf = buf
    self.offset = 0

  def status(self):
    """Return positional status."""
    o = self.offset
    l = len(self.buf)
    return { 'current': o, 'length': l, 'remainder': l-o }

  def readBytes(self, n):
    """Read n bytes and adjust offset for next read."""
    s = self.status()
    if s['remainder'] < n:
      raise ValueError('Offset is too large! (%d + %d > %d)' %
        (s['current'], n, s['length']))
    self.offset += n
    return self.buf[self.offset-n:self.offset]

  def readUInt8(self):
    """Read next byte as unsigned char."""
    return uint8(self.readBytes(1))

  def readUInt32(self):
    """Read four bytes as unsigned integer."""
    return uint32(self.readBytes(4))

  def readString(self):
    """Read the next string defined by: [uint32 length, string]"""
    return self.readBytes(self.readUInt32())