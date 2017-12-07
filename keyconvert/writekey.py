# Copyright Anton Semjonov, Licensed under GPL-3.0

from os.path import realpath

TINYSSH_FILENAME = {
  'ssh-ed25519': {
    'public': 'ed25519.pk',
    'secret': '.ed25519.sk',
  },
  'ecdsa-sha2-nistp256': {
    'public': 'nistp256ecdsa.pk',
    'secret': '.nistp256ecdsa.sk',
  },
}

KEYDIR = '/etc/tinyssh/sshkeydir'

def writekey(key, force, directory, verbose):
  for keypart in ('public', 'secret'):
    path = realpath('%s/%s' % (directory, TINYSSH_FILENAME[key.type][keypart]))
    with open(path, mode = 'wb' if force else 'xb') as out:
      if verbose:
        print('Writing %s/%s to %s' % (key.type, keypart, path))
      out.write(getattr(key, keypart))