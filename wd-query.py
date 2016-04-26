#!/usr/bin/python

"""wd-query.py - Query a package of wikidata

Usage: wd-query.py [-f label] <attribute> <packageFile>

Operate on a package of wikidata in packagefile. By default, list all labels of the named attribute in the package

Options:
    -f --find label  Search for the label in the given attribute and print a the matching item if found
"""

import json
import os
import sys

sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), "lib"))
from docopt           import docopt
from wikidata.package import Package

args    = docopt(__doc__, version='1.0')
package = Package(args["<packageFile>"])

if args["--find"]:
    item = package.find(args["<attribute>"], args["--find"])

    if not item:
        sys.exit("Label '%s' not found among %s in package %s" % (args["--find"], args["<attribute>"], args["<packageFile>"]))

    print json.dumps(item, sort_keys=True, indent=4, separators=(',', ': '))
    sys.exit(0)

for label in package.labels(args["<attribute>"]):
    try:
        print label
    except UnicodeError:
        print json.dumps(label)
