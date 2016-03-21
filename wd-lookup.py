#!/usr/bin/python

"""wd-lookup.py - look up entries in data extracted from a wikidata dump using an index

Usage: wd-lookup.py <key> <data> <index>
"""

import json
import os
import sys

sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), "lib"))
from docopt import docopt
from index  import Index

args  = docopt(__doc__, version='1.0')
idx   = Index(args["<index>"], args["<data>"])
key   = int(args["<key>"][1:]) if args["<key>"].startswith("Q") else int(args["<key>"])

try:
    entry = idx.get(key)
    print entry,
except KeyError:
    print "Key Q%d not found in index (minimum Q%d, maximum Q%d)" % (key, idx.first, idx.last)

sys.exit(0)

