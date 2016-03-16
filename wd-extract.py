#!/usr/bin/python

"""wd-extract.py - Extract data from a JSON dump of wikidata.org

Usage: wd-extract.py [-c|-C] [-DfnR] [-i file] [-l lc] [-o file] [-p lc] [-s pat] [-t type] [-w] <wd-dump-json>

Options:
    -C --claims         Don't simplify claims
    -c --classes        Extract the class hierarchy (requires simplifying the claims)
    -D --datatypes      Don't simplify datatypes
    -f --failonerror    If present, exit if an error occurs
    -i --index file     Output an index to file
    -l --language lc    Use language lc for all strings, falling back to en if needed, falling back to a random language if needed4
    -o --output file    Output the extraction to file
    -n --names          Print labels only instead of dumping objects in JSON
    -p --properties lc  Replace property ids with labels in language lc, falling back to english or a random language if needed
    -s --sitelinks pat  Pattern for sitelinks to include or "" to exclude all sitelinks
    -t --type type      Type of object to extract (property|item|id). Default=all
    -R --references     Don't remove references
    -w --warning        Print warnings
"""

import json
import os
import re
import struct
import sys

# Pick the the string for the requested language from a multilingual string map, falling back to English, or to the first string.
#
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

# Simple depluralize that only handles the cases it needs to
#
def depluralize(string):
    if string.endswith("ies"):
        return string[:-3] + "y"
    elif string.endswith("s"):
        return string[:-1]

    return string

# Extract the type and value (if any) a claim and return as {"type": <type>[, "value": <value>]}
#
def getClaimValue(claim):
    statement = {}

    try:
        if claim["mainsnak"]["snaktype"] == "novalue":
            statement["type"] = "novalue"
        elif claim["mainsnak"]["snaktype"] == "somevalue":
            statement["type"] = "somevalue"
        else:
            statementType = claim["mainsnak"]["datavalue"]["type"]

            if statementType == "string":
                statement = claim["mainsnak"]["datavalue"]["value"]
            elif statementType == "wikibase-entityid":
                statement["type"]  = claim["mainsnak"]["datavalue"]["value"]["entity-type"]
                statement["value"] = "P" if statement["type"] == "property" else "Q"
                statement["value"] += str(claim["mainsnak"]["datavalue"]["value"]["numeric-id"])
            else:
                statement["type"]  = statementType
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

    return statement

sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), "lib"))
from docopt  import docopt
from options import error, fatal, warn, options
args        = docopt(__doc__, version='1.0')
classId     = None
classes     = {} if args["--classes"] else None
indexFile   = open(args["--index"], "wb") if args["--index"] else None
keepClaims  = args["--claims"]
keepTypes   = args["--datatypes"]
lang        = args["--language"]
names       = args["--names"]
outputFile  = open(args["--output"], "w") if args["--output"] else sys.stdout
properties  = args["--properties"]
site        = args["--sitelinks"]
type        = args["--type"]
keepRefs    = args["--references"]
options["ignore-errors"] = not args["--failonerror"]
options["warning"]       = args["--warning"]

# If type is a class of item
#
if type and type.startswith("Q"):
    classId = type
    type    = "item"

if site and site != "":
    sitePat = re.compile(site + "$")

# If dumping the names of all objects and no language specified, default to English
#
if names and lang == None:
    lang = "en"

# Process the data file, extracting data by default and outputting it
#
def process(command="extract", output=outputFile):
    global indexFile
    wikidata   = open(args["<wd-dump-json>"])
    lineNum    = 0
    endOfLine  = "\n    "
    lastId     = 0
    outOfOrder = []

    while True:
        line    = wikidata.readline()
        lineNum += 1

        # Done?
        #
        if not line:
            break

        # Parse the next line, skipping the leading and trailing bracket lines
        #
        try:
            obj = json.loads(line[:-2])
        except:
            if len(line) == 2:
                if line[0] == "[":
                    continue
                elif line[0] == "]":
                    break
                else:
                    fatal("Unexpected line '%s'" % line[0], file=args["<wd-dump-json>"], line=lineNum)

            try:
                obj = json.loads(line[:-1])
            except:
                fatal("Unable to decode JSON in line '%s'" % line[:-1], file=args["<wd-dump-json>"], line=lineNum)

        # If generating a map of the properties
        #
        if command == "map":
            if obj["type"] != "property":
                continue

            if obj["id"] == "P279":
                if "en" not in obj["labels"]:
                    fatal("Property P279 does not have an English label (expected 'subclass of')")

                if obj["labels"]["en"]["value"] != "subclass of":
                    fatal("Property P279 has English label '%s' (expected 'subclass of')" % obj["labels"]["en"]["value"])

            try:
                output.write(endOfLine + '"' + obj["id"] + '": ' + json.dumps(chooseString(obj["labels"], properties)))
            except KeyError:
                error("Object %s has no label" % obj["id"], file=args["<wd-dump-json>"], line=lineNum)

            endOfLine = ",\n    "
            continue

        # If filtering by type (either just properties or just items), skip if not the one we want.
        #
        if type and obj["type"] != type:
            continue

        # Skip objects that don't have an id (with an error)
        #
        if "id" not in obj:
            error("object has no id", file=args["<wd-dump-json>"], line=lineNum)
            continue

        # If filtering by class
        #
        if classId:
            if "claims" not in obj or "P31" not in obj["claims"]:
                warn("Object '%s' has no class (claim with property P31)" % obj["id"], file=args["<wd-dump-json>"], line=lineNum)
                continue

            match = False

            for claim in obj["claims"]["P31"]:
                statement = getClaimTypeAndValue(claim)

                try:
                    if statement["value"] == classId:
                        match = True
                        break
                except KeyError:
                    error("Object '%s' has a class with no value: %s" % (obj["id"], str(statement)), file=args["<wd-dump-json>"],
                          line=lineNum)

            if not match:
                continue

        # Collapse multilingual string tables if desired.
        #
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

        # If listing the labels, do it
        #
        if names:
            try:
                print obj["label"]
            except UnicodeEncodeError:
                print json.dumps(obj["label"])
            except KeyError:
                error("Object %s has no label" % obj["id"], file=args["<wd-dump-json>"], line=lineNum)

            continue

        # Unless told not to, simplify the "claims" (i.e. the properties of the object)
        #
        if not keepClaims and "claims" in obj:
            # For each property that has claims
            #
            for property in obj["claims"]:
                label = property    # Default property name to the id

                # If substituting labels for property ids, look the label up in the map
                #
                if properties:
                    try:
                        label = properties[property]
                    except KeyError:
                        warn("Property '%s' not in map" % property, file=args["<wd-dump-json>"], line=lineNum)

                obj[label] = []

                # For each claim of this property
                #
                for claim in obj["claims"][property]:
                    obj[label].append(getClaimValue(claim))

                if classes != None and property == "P279":
                    classes[obj["id"]] = {"subclass of": []}

                    for item in obj[label]:
                        if item["type"] != "item":
                            error("Expected type of class to be 'item', got '%s'" % item["type"], file=args["<wd-dump-json>"],
                                  line=lineNum)

                        try:
                            classes[obj["id"]]["subclass of"].append(item["value"])
                        except KeyError:
                            warn("Class has no value: " + json.dumps(item), file=args["<wd-dump-json>"], line=lineNum)
                            classes[obj["id"]]["subclass of"].append(item)

                    try:
                        if lang:
                            classes[obj["id"]]["label"]  = obj["label"]
                        else:
                            classes[obj["id"]]["labels"] = obj["labels"]

                    except KeyError:
                        warn("Class %s has no label%s" % (obj["id"], "" if lang else "s"), file=args["<wd-dump-json>"],
                             line=lineNum)

            del obj["claims"]

        # If a sitelink filter was specified, apply it
        #
        if site != None and "sitelinks" in obj:
            if site == "":
                del obj["sitelinks"]
            else:
                for link in obj["sitelinks"].keys():
                    if not sitePat.match(link):
                        del obj["sitelinks"][link]

        # Prepare the index entry unless its out of order
        if indexFile != None:
            indexOffset = output.tell()
            indexId     = int(obj["id"][1:])

        json.dump(obj, output, sort_keys=True, separators=(',', ':'))
        output.write("\n")

        # Complete the index entry and write it if in order, otherwise save for sort/merge
        if indexFile != None:
            indexBytes = struct.pack(">QQQ", indexId, indexOffset, output.tell() - indexOffset)

            if indexId < lastId:
                warn("Item id %d comes after %d in the dump: out of order ids" % (indexId, lastId), file=args["<wd-dump-json>"],
                     line=lineNum)
                outOfOrder.append(indexBytes)

            else:
                indexFile.write(indexBytes)
                lastId = indexId

        endOfLine = ",\n    "

    if len(outOfOrder) == 0:
        return

    error("Number of OOO elements = %d" % len(outOfOrder))

    indexFile.close()
    outOfOrder.sort()
    os.rename(args["--index"], args["--index"] + ".part")
    partFile  = open(args["--index"] + ".part", "rb")
    indexFile = open(args["--index"], "wb")
    nextOOO   = 0
    nextPart  = partFile.read(24)

    while nextPart:
        if nextOOO < len(outOfOrder) and outOfOrder[nextOOO] < nextPart:
            indexFile.write(outOfOrder[nextOOO])
            nextOOO += 1
            continue

        indexFile.write(nextPart)
        nextPart = partFile.read(24)

    error("Index file size %d, number of OOO elements %d, number left %d"
          % (indexFile.tell(), len(outOfOrder), len(outOfOrder) - nextOOO))

    while nextOOO < len(outOfOrder):
        indexFile.write(outOfOrder[nextOOO])
        nextOOO += 1

#
# Main entry point
#

# If the properties are to be substituted, build a map first
#
if properties:
    if args["<wd-dump-json>"].endswith(".json"):
        propFileName = args["<wd-dump-json>"][:-5] + "-properties.json"
    else:
        propFileName = args["<wd-dump-json>"] + "-properties.json"

    if not os.path.exists(propFileName):
        propFile = open(propFileName, "w")
        propFile.write("{")
        process(command="map", output=propFile)
        propFile.write("\n}\n")
        propFile.close()

    properties = json.load(open(propFileName))

    if "P31" not in properties:
        fatal("Property P31 (instance of) not found!")

    if "P279" not in properties:
        fatal("Property P279 (subclass of) not found!")

# Now extract the data (or list the labels) and optionally, the index
#
process()
outputFile.close()

if indexFile:
    indexFile.close()

# If dumping the class hierarchy, do so
#
if classes:
    if args["<wd-dump-json>"].endswith(".json"):
        classFileName = args["<wd-dump-json>"][:-5] + "-classes.json"
    else:
        classFileName = args["<wd-dump-json>"] + "-classes.json"

    if not os.path.exists(classFileName):
        output = open(classFileName, "w")
        json.dump(classes, output, sort_keys=True, indent=4, separators=(',', ': '))
        output.close()

