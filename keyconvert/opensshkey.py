# Copyright Anton Semjonov, Licensed under GPL-3.0

from base64 import b64encode as base64
from json import dumps as json
from sys import stderr

from keyconvert.arguments import args
from keyconvert.buffer import Buffer
from keyconvert.readkey import readkey
from keyconvert.writekey import writekey

class OpenSSHKey:
  """Read a key from $filename and parse its contents
  if it is an OpenSSH compatible secretkey."""

  @staticmethod
  def __check_encryption(buf):
    """Cipher and KDF need to be none,
    i.e. the key must not be encrypted!"""
    if buf.readString() != b'none':
      raise ValueError("Cipher is not 'none'!")
    if buf.readString() != b'none':
      raise ValueError("KDF is not 'none'!")
    if buf.readString() != b'':
      raise ValueError("KDF options are not empty!")

  @staticmethod
  def __check_singlekey(buf):
    """Check that the number of keys is equal to 1."""
    if buf.readUInt32() != 1:
      raise ValueError("More than one key inside!")

  @staticmethod
  def __check_secret_magic(blob):
    """Check that there are two identical uint32's at the beginning
    of the secretkey blob, indicating successful 'decryption'."""
    if blob.readUInt32() != blob.readUInt32():
      raise ValueError('Magic numbers in secretkey blob do not match!')

  @staticmethod
  def __check_secret_padding(blob):
    """Check that the Padding at the end of the secret
    key blob is an incrementing sequence <= blocksize."""
    for i in range(blob.status()['remaining']):
      if i > 255 or blob.readUInt8() != i+1:
        raise ValueError('Padding at the end of the secretkey blob is incorrect!')
    blob.close()

  @staticmethod
  def __get_secret_blob(buf):
    """Get secretkey blob and check that there is no additional
    data at the end of the buffer."""
    blob = Buffer(buf.readString())
    if buf.status()['remaining'] != 0:
      raise ValueError('There is data after the secretkey blob!')
    buf.close()
    return blob

  def __init__(self, filename=args.key):

    buf = readkey(filename)

    # check prerequisites
    self.__check_encryption(buf)
    self.__check_singlekey(buf)

    # ignore public key
    buf.readString()

    # get secret key blob
    blob = self.__get_secret_blob(buf)

    # check magic numbers
    self.__check_secret_magic(blob)

    # parse key contents
    self.__parseSecretBlob(blob)

    # check padding
    self.__check_secret_padding(blob)


  def __parseSecretBlob(self, blob):
    """Parse a secretkey blob and set contents."""
    
    # key type
    self.type     = blob.readString().decode('utf-8')
    
    # curve
    if self.type == 'ssh-ed25519':
      self.curve = 'ed25519'
      self.public   = blob.readString()
      self.secret   = blob.readString()

    elif self.type == 'ecdsa-sha2-nistp256':
      print('WARNING: ECDSA key support is incomplete and incompatible with tinyssh!', file=stderr)
      # since version 20190101 tinyssh deprecated and removed ecdsa anyway ...
      self.curve    = blob.readString().decode('utf-8')
      coordinates   = Buffer(blob.readString())
      is_compressed = coordinates.readUInt8()
      if is_compressed != 0x04:
        print('the ecdsa coordinates are not in compressed form!')
      x = coordinates.readBytes(32)
      y = coordinates.readBytes(32)
      self.secret = x + y
      self.public = blob.readString()

    else:
      raise ValueError('Unknown key type: %s' % self.type)
    
    # comment
    self.comment  = blob.readString().decode('utf-8')

    if args.verbose:
      print('Successfully read %s key (%s).' % (self.type, self.comment))

  def toJSON(self):
    return json({
      'type': self.type,
      'curve': self.curve,
      'public': base64(self.public).decode('utf-8'),
      'secret': base64(self.secret).decode('utf-8'),
      'comment': self.comment,
    }, indent=2)

  def write(self, directory):
    writekey(self, args.force, directory, args.verbose)