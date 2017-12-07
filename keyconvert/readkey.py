# Copyright Anton Semjonov, Licensed under GPL-3.0

from base64 import b64decode
from keyconvert.buffer import Buffer

def readkey (file):
  """Read OpenSSH-Key-V1 compatible file and return
  a Buffer of its contents."""

  with file as keyfile:
    armor = keyfile.read().split('\n')
  string = ''


  BEGINTAG = '-----BEGIN OPENSSH PRIVATE KEY-----'
  ENDTAG   = '-----END OPENSSH PRIVATE KEY-----'

  for index, line in enumerate(armor):

    if index == 0:
      # first line must have the begin tag
      if line != BEGINTAG:
        raise ValueError('Not a compatible file!')
      else:
        continue

    if index == (len(armor)-1) and line != ENDTAG:
      # reached last line with no end tag
      raise ValueError('Partial file? No end tag!')

    if line == ENDTAG:
      # reached end tag, break loop
      break

    # default action: concatenate base64 string
    string += line

  bytestring = b64decode(string)
  key = Buffer(bytestring)

  OPENSSH_TAG = b'openssh-key-v1\x00'
  if key.readBytes(len(OPENSSH_TAG)) == OPENSSH_TAG:
    return key
  else:
    raise ValueError('Not an OpenSSH V1 key!')