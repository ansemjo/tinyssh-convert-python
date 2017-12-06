import json
from os import path

ROOTDIR = path.dirname(path.realpath(__file__)) + '/../'

def __loadJSON(filename):
  return json.load(open(path.realpath(ROOTDIR + filename), mode='r'))

"""package.json contents from project root."""
package = __loadJSON('package.json')