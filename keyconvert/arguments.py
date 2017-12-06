from argparse import ArgumentParser

from keyconvert.package import package

def arguments():
  """Parse commandline-arguments."""

  # init
  parser = ArgumentParser(
    description=package['description'],
    epilog='%(name)s v%(version)s (%(author)s)' %
      {
        'name'    : package['name'],
        'version' : package['version'],
        'author'  : package['author'],
      }
  )

  # source file
  parser.add_argument('-k', '--key', help='OpenSSH secret key', required=True)
  
  return parser.parse_args()
