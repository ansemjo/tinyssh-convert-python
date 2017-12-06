from struct import unpack

class Buffer:

  def __init__(self, buf):
    self.buf = buf
    self.offset = 0

  def readBytes(self, n):
    #print(f'({self.offset} +{n}, {len(self.buf)})', end=' ')
    self.offset += n
    slice = self.buf[self.offset-n:self.offset]
    #print(slice)
    return slice

  def readUInt32(self):
    bytes = self.readBytes(4)
    return unpack('>L', bytes)[0]

  def readString(self):
    return self.readBytes(self.readUInt32())