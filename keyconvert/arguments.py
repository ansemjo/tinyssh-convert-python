from argparse import ArgumentParser, FileType

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

  # be verbose
  parser.add_argument('-v', '--verbose',
    help='be verbose',
    action='store_true',
  )
  
  # /** group: inputs **/
  group_input = parser.add_argument_group('input')

  # source file
  group_input.add_argument('-k', '--key',
    type=FileType('r'),
    help='openssh secret key',
    required=True,
  )

  # /** group: outputs **/
  group_output = parser.add_argument_group('output')

  # write to directory
  group_output.add_argument('-d', '--dir',
    help='write key files to destination directory',
  )

  # overwrite existing files
  group_output.add_argument('-f', '--force',
    help='overwrite existing files',
    action='store_true',
  )

  # echo json representation
  group_output.add_argument('-j', '--json',
    help='output a json representation to stdout',
    action='store_true',
  )

  return parser.parse_args()

args = arguments()
