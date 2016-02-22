#!/usr/bin/python

"""wd-extract.py - Extract data from a JSON dump of wikidata.org

Usage: wd-extract.py [-cfnpr] [-l lc] [-s pat] [-w] <wd-dump-json>

Options:
    -c --claims         Don't simplify claims
    -f --failonerror    If present, exit if an error occurs
    -l --language lc    Use lc for all strings, falling back to en if needed, falling back to a random language if needed
    -n --names          Print lables only instead of dumping objects in JSON
    -p --properties     Just dump the properties
    -s --sitelinks pat  Pattern for sitelinks to include or "" to exclude all sitelinks
    -r --references     Don't remove references
    -w --warning        Print warnings
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
from options import error, fatal, warn, options
args   = docopt(__doc__, version='1.0')
claims = args["--claims"]
lang   = args["--language"]
names  = args["--names"]
props  = args["--properties"]
site   = args["--sitelinks"]
refs   = args["--references"]
options["ignore-errors"] = not args["--failonerror"]
options["warning"]       = args["--warning"]

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

    if props and obj["type"] != "property":
        continue

    if names:
        try:
            print obj["label"]
        except KeyError:
            error("object %s has no label" % obj["id"], file=args["<wd-dump-json>"], line=lineNum)

        continue

    if "id" not in obj:
        error("object has no id", file=args["<wd-dump-json>"], line=lineNum)
        continue

    if lang:
        for member in ("labels", "descriptions", "aliases"):
            if member not in obj:
                warn("object has no %s" % member, file=args["<wd-dump-json>"], line=lineNum)
                continue

            if lang in obj[member]:
                value = obj[member][lang]
            elif "en" in obj[member]:
                value = obj[member][lang]
            elif len(obj[member]) > 0:
                value = obj[member][obj[member].keys()[0]]
            else:
                warn("object member %s contains no string in any language" % member, file=args["<wd-dump-json>"], line=lineNum)
                del obj[member]
                continue

            if isinstance(value, list):
                obj[member] = []

                for element in value:
                    obj[member].append(element["value"])

            else:
                del obj[member]
                obj[depluralize(member)] = value["value"]

    if not claims and "claims" in obj:
        for property in obj["claims"]:
            obj[property] = []

            for claim in obj["claims"][property]:
                statement = {}

                try:
                    if claim["mainsnak"]["snaktype"] == "novalue":
                        statement["type"] = "novalue"
                    elif claim["mainsnak"]["snaktype"] == "somevalue":
                        statement["type"] = "somevalue"
                    elif claim["mainsnak"]["datavalue"]["type"] == "wikibase-entityid":
                        statement["type"]  = claim["mainsnak"]["datavalue"]["value"]["entity-type"]
                        statement["value"] = "P" if statement["type"] == "property" else "Q"
                        statement["value"] += str(claim["mainsnak"]["datavalue"]["value"]["numeric-id"])
                    else:
                        statement["type"]  = claim["mainsnak"]["datavalue"]["type"]
                        statement["value"] = claim["mainsnak"]["datavalue"]["value"]

                except KeyError:
                    if "mainsnak" not in claim:
                        error("property %s claim has no mainsnak" % property, file=args["<wd-dump-json>"], line=lineNum)
                    elif "datavalue" not in claim["mainsnak"]:
                        error("property %s claim mainsnak has no datavalue" % property, file=args["<wd-dump-json>"], line=lineNum)
                    elif "type" not in claim["mainsnak"]["datavalue"]:
                        error("property %s claim mainsnak datavalue has no type" % property, file=args["<wd-dump-json>"], line=lineNum)
                    elif "value" not in claim["mainsnak"]["datavalue"]:
                        error("property %s claim mainsnak datavalue of type %s has no value"
                            % (property, claim["mainsnak"]["datavalue"]["type"]), file=args["<wd-dump-json>"], line=lineNum)

                    fatal("claim:" + json.dumps(claim, sort_keys=True, indent=4, separators=(',', ': ')))

                obj[property].append(statement)

    if site != None and "sitelinks" in obj:
        if site == "":
            del obj["sitelinks"]
        else:
            for link in obj["sitelinks"].keys():
                if not sitePat.match(link):
                    del obj["sitelinks"][link]

    print json.dumps(obj, sort_keys=True, indent=4, separators=(',', ': '))
