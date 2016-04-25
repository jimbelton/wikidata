#!/usr/bin/python

"""wd-query.py - Query a package of wikidata

Usage: wd-query.py <attribute> <packageFile>

List all labels of the named attribute in the packageFile
"""

import os
import sys

sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), "lib"))
from docopt           import docopt
from wikidata.package import Package

args    = docopt(__doc__, version='1.0')
package = Package(args["<packageFile>"])

for label in package.labels("books"):
    print label
