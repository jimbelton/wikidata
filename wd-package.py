#!/usr/bin/python

"""wd-package.py - Generate a package of data from data extracted from a wikidata dump

Usage: wd-package.py [-l languages] <class> <data> <index>

Options:
    -l --languages list    Include only books in one of the comma separated list of languages (default=all). e.g. "English,German"
"""

import json
import os
import sys

unwantedProperties = {
#    "BNCF Thesaurus",                        # Florentine national central library
#    "BnF identifier",                        # French national library
#    "Commons category",                      # Wikimedia Commons
#    "Commons gallery",                       # Wikimedia Commons
#    "Freebase identifier",                   # Defunct structured data source, purchased and closed by Google
#    "GND identifier",                        # German universal authority file
#    "IMDb identifier",                       # Internet movie database
#    "ISFDB title ID",                        # Internet speculative fiction database
#    "KINENOTE film ID",                      # Japanese KINENOTE movie database
#    "LCAuth identifier",                     # US libary of congress
#    "Library of Congress Classification",    # US libary of congress
#    "LibraryThing work identifier",          # LibraryThing
#    "MusicBrainz artist ID",                 # MusicBrainz
#    "MusicBrainz release group ID",          # MusicBrainz
#    "MusicBrainz work ID",                   # MusicBrainz
#    "NDL identifier",                        # Japan national diet library
#    "NLA (Australia) identifier",            # Australian national library
#    "OCLC control number",                   # WorldCat
#    "Open Library identifier",               # openlibrary.org
#    "PSH ID",                                # Czech technical library
#    "Regensburg Classification",             # German university of Regensburg library
#    "SUDOC authorities",                     # French university libraries
#    "VIAF identifier"                        # Virtual international authority file
}

# For each package, the map of properties that point to other objects to the names of collections of those objects.
#
objectProperties = {
    "books": {"author":                     "authors",
              "award recieved":             "awards",
              "country of origin":          "countries",
              "creator":                    "creators",
              "genre":                      "genres",
              "nominated for":              "nominations",
              "original language of work":  "languages",
              "publisher":                  "publishers",
              "series":                     "series"}
}

sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), "lib"))
#import simplify
from docopt  import docopt
from index   import Index
from options import options, error, warn
options["ignore-errors"] = True
args      = docopt(__doc__, version='1.0')
data      = open(args["<data>"])
index     = Index(args["<index>"], args["<data>"])
languages = set(args["--languages"].split(',')) if args["--languages"] else None
classIds  = set()
lineNum   = 0

if args["<class>"][:1] == "Q":
    classIds.add(args["<class>"])

elif args["<class>"] == "books":
    classIds.add("Q571")

else:
    sys.exit("%s: Class '%s' should be Q#### or books" % (__file__, args["<class>"]))

itemCache = {}
package   = {"items": {}, args["<class>"]: {}}

# Get an item, either from the package, the cache, or the extracted data
#
def getItem(itemId):
    if itemId in package["items"]:
        return package["items"][itemId]

    if itemId not in itemCache:
        try:
            itemCache[itemId] = json.loads(index.get(int(itemId[1:])))    # The index uses integer ids
        except KeyError:
            error("Item %s was not found in the extracted data index" % itemId, file=args["<data>"], line=lineNum)
            return {"label": itemId}

    return itemCache[itemId]

# Process the extracted data, looking for base types in the package (e.g. books)
#
for line in data:
    lineNum += 1
    object   = json.loads(line)
    classId  = None

    if "instance of" not in object:
        continue

    for clazz in object["instance of"]:
        try:
            if clazz["value"] in classIds:
                classId = clazz["value"]
        except KeyError:
            warn("Item '%s' is an intance of 'no value'" % object["label"], file=args["<data>"], line=lineNum)
            continue

    if classId == None:
        continue

    for property in object.keys():
        if property in unwantedProperties:
            del object[property]
            continue

        # Walk across the array of values backward, so that deletions don't screw up the traversal
        for i in reversed(xrange(len(object[property]))):
            value = object[property][i]

            # If value is a complex type
            if isinstance(value, dict) and "type" in value:
                if value["type"] == "item":
                    try:
                        object[property][i] = getItem(value["value"])["label"]
                    except KeyError:
                        error("Item '%s' property %s has a value that is item '%s' that has no label"
                              % (object["label"], property, value['value']), file=args["<data>"], line=lineNum)
                        object[property][i] = value["value"]
                elif value["type"] == "novalue":
                    if len(object[property]) != 1:
                        error("Item '%s' property %s has 'novalue' in addition to other values" % (object["label"], property),
                              file=args["<data>"], line=lineNum)
                        del object[property][i]
                    else:
                        del(object[property])
                elif value["type"] == "somevalue":
                    if len(object[property]) != 1:
                        warn("Item '%s' property %s has 'somevalue' in addition to other values" % (object["label"], property),
                              file=args["<data>"], line=lineNum)
                        del object[property][i]
                    else:
                        object[property] = None    # None represents "somevalue", AKA unknown
                #else:
                #    error("Item '%s' property %s contains a bad object: %s" % (object["label"], property, str(value)),
                #          file=args["<data>"], line=lineNum)

    # If we're filtering the languages and this in not one that we want, skip it
    if languages and "original language of work" in object:
        if len(set(object["original language of work"]) & languages) == 0:
            try:
                error("Item '%s' is in language '%s'" % (object["label"], ",".join(object["original language of work"])))
            except UnicodeEncodeError:
                try:
                    error("Item '%s' is in language '%s'"
                          % (json.dumps(object["label"]), ",".join(object["original language of work"])))
                except UnicodeEncodeError:
                    error("Item '%s' is in language '%s'"
                          % (json.dumps(object["label"]),
                             ",".join([json.dumps(language) for language in object["original language of work"]])))

    package["items"        ][object["id"]] = object
    package[args["<class>"]][object["id"]] = None
    del object["id"]

print json.dumps(package, sort_keys=True, indent=4, separators=(',', ': '))
