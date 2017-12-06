from buffer import Buffer
from base64 import b64encode as base64
from json import dumps as json

class SecKey:

  def __init__(self, buf: Buffer):

    # check that key is not encrypted
    if buf.readString() != b'none':
      raise ValueError("Cipher is not 'none'!")
    if buf.readString() != b'none':
      raise ValueError("KDF is not 'none'!")
    if buf.readString() != b'':
      raise ValueError("KDF options are not empty!")

    # check that only one key is present
    if buf.readUInt32() != 1:
      raise ValueError("More than one key inside!")

    # ignore public key
    buf.readString()

    # secret key blob
    blob = Buffer(buf.readString())
    self.blob = blob

    # check magic numbers
    if blob.readUInt32() != blob.readUInt32():
      raise ValueError("Magic Numbers in Secretkey blob do not match!")

    self.type = blob.readString()
    self.public = blob.readString()
    self.secret = blob.readString()
    self.comment = blob.readString()

  def toJSON(self):
    return json({
      "type": self.type.decode('utf-8'),
      "public": base64(self.public).decode('utf-8'),
      "secret": base64(self.secret).decode('utf-8'),
      "comment": self.comment.decode('utf-8')
    }, indent=2)