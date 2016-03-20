#!/usr/bin/python

"""wd-package.py - Generate a package of data from data extracted from a wikidata dump

Usage: wd-package.py <class> <data> <index>
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
    "KINENOTE film ID"                      # Japanese KINENOTE movie database
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
              "award recieved",             "awards",
              "country of origin",          "countries",
              "creator":                    "creators",
              "genre":                      "genres",
              "nominated for",              "nominations",
              "original language of work":  "languages",
              "publisher":                  "publishers",
              "series":                     "series"}
}

sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), "lib"))
import simplify
from docopt  import docopt
from index   import Index
from options import options, error, warn
options["ignore-errors"] = True
args     = docopt(__doc__, version='1.0')
data     = open(args["<data>"])
index    = Index(args["<index>"], args["<data>"])
classIds = set()
lineNum  = 0

if args["<class>"][:1] == "Q":
    classIds.add(args["<class>"])

elif args["<class>"] == "books":
    classIds.add("Q571")

else:
    sys.exit("%s: Class '%s' should be Q#### or books" % (__file__, args["<class>"]))

package  = {"items": {}, args["<class>"]: {}}

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

        # Walk across the array of values
        for i, value in enumerate(object[property]):
            # If value is a complex type
            if isinstance(value, dict) and "type" in value:
                if value["type"] == "item":
                    object[property][i] = value["value"]
                elif value["type"] == "novalue":
                    if len(object[property]) != 1:
                        error("Item '%s' property %s has 'novalue' in addition to other values" % (object["label"], property),
                              file=args["<data>"], line=lineNum)
                    else:
                        del(object[property])
                elif value["type"] == "somevalue":
                    if len(object[property]) != 1:
                        error("Item '%s' property %s has 'somevalue' in addition to other values" % (object["label"], property),
                              file=args["<data>"], line=lineNum)
                    else:
                        object[property] = None    # None represents "somevalue", AKA unknown
                elif value["type"] == "time":
                    object[property] = simplify.time(value)

                #else:
                #    error("Item '%s' property %s contains a bad object: %s" % (object["label"], property, str(value)),
                #          file=args["<data>"], line=lineNum)

    package["items"        ][object["id"]] = object
    package[args["<class>"]][object["id"]] = None
    del object["id"]

print json.dumps(package, sort_keys=True, indent=4, separators=(',', ': '))
