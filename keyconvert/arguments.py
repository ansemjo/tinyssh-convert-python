# Copyright Anton Semjonov, Licensed under GPL-3.0

from argparse import ArgumentParser, FileType

from keyconvert.package import package as p

def arguments():
  """Parse commandline-arguments."""

  # init
  parser = ArgumentParser(
    description=p['description'],
    epilog='Version %(version)s (Copyright %(year)s %(author)s, Licensed under %(license)s)' %
      {
        'name'    : p['name'],
        'version' : p['version'],
        'author'  : p['author'],
        'license' : p['license'],
        'year'    : p['license_years'],
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
