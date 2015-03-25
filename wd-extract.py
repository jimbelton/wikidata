#!/usr/bin/python

"""wd-extract.py - Extract data from a JSON dump of wikidata.org

Usage: wd-extract.py [-f] [-l lc] [-s pat] <wd-dump-json>

Options:
    -f --failonerror    If present, exit if an error occurs
    -l --language lc    Use lc for all strings, falling back to en if needed, falling back to a random language if needed.
    -s --sitelinks pat  Pattern for sitelinks to include or "" to exclude all sitelinks
"""

import json
import os
import re
import sys

def depluralize(string):
    if string.endswith("ies"):
        return string[:-3] + "y"
    elif string.endswith("s"):
        return string[:-1]

    return string

sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), "lib"))
from docopt  import docopt
from options import error, warn, options
args = docopt(__doc__, version='1.0')
lang = args["--language"]
site = args["--sitelinks"]
options["ignore-errors"] = not args["--failonerror"]

if site and site != "":
    sitePat = re.compile(site + "$")

wikidata = open(args["<wd-dump-json>"])
lineNum  = 0

while True:
    line    = wikidata.readline()
    lineNum += 1

    if not line:
        break

    if line.strip() == "[":
        continue

    obj = json.loads(line[:-2])

    if "id" not in obj:
        error("object has no id", file=args["<wd-dump-json>"], line=lineNum)
        continue

    if lang:
        for member in ("labels", "descriptions", "aliases"):
            if member not in obj:
                warn( "object has no %s" % member, file=args["<wd-dump-json>"], line=lineNum)
                continue

            if lang in obj[member]:
                value = obj[member][lang]
            elif "en" in obj[member]:
                value = obj[member][lang]
            else:
                value = obj[member][obj[member].keys()[0]]

            if isinstance(value, list):
                obj[member] = []

                for element in value:
                    obj[member].append(element["value"])

            else:
                del obj[member]
                obj[depluralize(member)] = value["value"]

    if site != None and "sitelinks" in obj:
        if site == "":
            del obj["sitelinks"]
        else:
            for link in obj["sitelinks"].keys():
                if not sitePat.match(link):
                    del obj["sitelinks"][link]

    print json.dumps(obj, sort_keys=True, indent=4, separators=(',', ': '))


