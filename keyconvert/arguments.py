from argparse import ArgumentParser

def Arguments():
  """Parse commandline-arguments."""

  # init
  parser = ArgumentParser()

  # source file
  parser.add_argument('-k', '--key', help='OpenSSH secret key', required=True)
  
  return parser.parse_args()
