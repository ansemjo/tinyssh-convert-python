from base64 import b64decode
from keyconvert.buffer import Buffer

def readkey (filename):
  armor = open(filename, mode='r').read()

  BEGINTAG = '-----BEGIN OPENSSH PRIVATE KEY-----'
  ENDTAG   = '-----END OPENSSH PRIVATE KEY-----'
  string = ''

  for line in armor.split('\n'):
    
    if line == BEGINTAG:
      flag = True
      continue

    if line == ENDTAG:
      flag = False
      break

    if flag is True:
      string += line

  bytestring = b64decode(string)
  key = Buffer(bytestring)

  OPENSSH_TAG = b'openssh-key-v1\x00'
  if key.readBytes(len(OPENSSH_TAG)) == OPENSSH_TAG:
    return key
  else:
    raise ValueError('Not an OpenSSH key')