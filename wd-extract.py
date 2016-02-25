#!/usr/bin/python

"""wd-extract.py - Extract data from a JSON dump of wikidata.org

Usage: wd-extract.py [-cfnr] [-l lc] [-p lc] [-s pat] [-t type] [-w] <wd-dump-json>

Options:
    -c --claims         Don't simplify claims
    -f --failonerror    If present, exit if an error occurs
    -l --language lc    Use language lc for all strings, falling back to en if needed, falling back to a random language if needed
    -n --names          Print lables only instead of dumping objects in JSON
    -p --properties lc  Replace property ids with labels in language lc, falling back to english or a random language if needed
    -s --sitelinks pat  Pattern for sitelinks to include or "" to exclude all sitelinks
    -t --type type      Type of object to extract (property|item). Default=all
    -r --references     Don't remove references
    -w --warning        Print warnings
"""

import json
import os
import re
import sys

def chooseString(strings, language):
    if language in strings:
        value = strings[language]

    elif "en" in strings:
        value = strings["en"]

    elif len(strings) > 0:
        value = strings[strings.keys()[0]]

    else:
        return None

    if isinstance(value, list):
        newValue = []

        for element in value:
            newValue.append(element["value"])

        return newValue

    return value["value"]

def depluralize(string):
    if string.endswith("ies"):
        return string[:-3] + "y"
    elif string.endswith("s"):
        return string[:-1]

    return string

sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), "lib"))
from docopt  import docopt
from options import error, fatal, warn, options
args       = docopt(__doc__, version='1.0')
claims     = args["--claims"]
lang       = args["--language"]
names      = args["--names"]
properties = args["--properties"]
site       = args["--sitelinks"]
type       = args["--type"]
refs       = args["--references"]
options["ignore-errors"] = not args["--failonerror"]
options["warning"]       = args["--warning"]

if site and site != "":
    sitePat = re.compile(site + "$")

def process(command="extract", output=sys.stdout):
    wikidata  = open(args["<wd-dump-json>"])
    lineNum   = 0
    endOfLine = "\n    "

    while True:
        line    = wikidata.readline()
        lineNum += 1

        if not line:
            break

        if len(line) == 2:
            if line[0] == "[":
                continue
            elif line[0] == "]":
                break
            else:
                fatal("Unexpected line '%s'" % line[0], file=args["<wd-dump-json>"], line=lineNum)

        try:
            obj = json.loads(line[:-2])
        except:
            try:
                obj = json.loads(line[:-1])
            except:
                fatal("Unable to decode JSON '%s'" % line[:-2], file=args["<wd-dump-json>"], line=lineNum)

        if command == "map":
            if obj["type"] != "property":
                continue

            try:
                #output.write(endOfLine + '"' + obj["id"] + '"')
                output.write(endOfLine + '"' + obj["id"] + '": ' + json.dumps(chooseString(obj["labels"], properties)))
            except KeyError:
                error("Object %s has no label" % obj["id"], file=args["<wd-dump-json>"], line=lineNum)

            endOfLine = ",\n    "
            continue

        if type and obj["type"] != type:
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

                value = chooseString(obj[member], lang)
                del obj[member]

                if value == None:
                    warn("object member %s contains no string in any language" % member, file=args["<wd-dump-json>"], line=lineNum)

                elif isinstance(value, list):
                    obj[member] = value

                else:
                    obj[depluralize(member)] = value

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

if properties:
    if args["<wd-dump-json>"].endswith(".json"):
        mapFileName = args["<wd-dump-json>"][:-5] + "-properties.json"
    else:
        mapFileName = args["<wd-dump-json>"] + "-properties.json"

    if not os.path.exists(mapFileName):
        output = open(mapFileName, "w")
        output.write("{")
        process(command="map", output=output)
        output.write("\n}\n")
        output.close()

    properties = json.load(open(mapFileName))

process()
