#!/usr/bin/python

"""wd-package.py - Generate a package of data from data extracted from a wikidata dump

Usage: wd-package.py [-l languages] <class> <data> <index>

Options:
    -l --languages list    Include only books in one of the comma separated list of languages (default=all). e.g. "en,de".
                           If no 'original language of work' is specified and the book does not have a label in the requested
                           language, don't include it. This requires that the extraction being used has multilingual strings ('-l'
                           was not specified) or has label languages preserved ('-L' was specified).
"""

import json
import os
import sys

unwantedProperties = {
}

# For each package, the map of properties that point to other objects to the names of collections of those objects.
#
objectProperties = {
    "books": {
        "class":                      "Q571",
        "author":                     "authors",
        "award recieved":             "awards",
        "country of origin":          "countries",
        "creator":                    "creators",
        "genre":                      "genres",
        "nominated for":              "nominations",
        "original language of work":  "languages",
        "publisher":                  "publishers",
        "series":                     "series"
    }
}

sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), "lib"))
#import simplify
from docopt  import docopt
from index   import Index
from options import options, error, fatal, warn
import language

options["ignore-errors"] = True
args      = docopt(__doc__, version='1.0')
data      = open(args["<data>"])
index     = Index(args["<index>"], args["<data>"])
languages = set(args["--languages"].split(',')) if args["--languages"] else None
classIds  = set()
lineNum   = 0

if args["<class>"][:1] == "Q":
    classIds.add(args["<class>"])

elif args["<class>"] in objectProperties:
    classIds.add(objectProperties[args["<class>"]]["class"])

else:
    fatal("Class '%s' should be Q#### or in {%s}" % (args["<class>"], ",".join(objectProperties.keys())))

itemCache = {}
package   = {"items": {}, args["<class>"]: []}

if args["<class>"] in objectProperties:
    objectProperties = objectProperties[args["<class>"]]
else:
    objectProperties = {}

for property in objectProperties:
    package[property] = []

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

    if "label" not in object:
        error("Item %s is a %s but has no label" % (object["id"], args["<class>"]), file=args["<data>"], line=lineNum)
        continue

    # If we're filtering the languages
    #
    if languages:

        # If the label's language has been preserved, use it
        if isinstance(object["label"], dict):
            if object["label"]["language"] not in languages:
                warn("Item '%s' label language is '%s': skipped" % (object["label"]["value"], object["label"]["language"]),
                     file=args["<data>"], line=lineNum)
                continue

            object["label"] = object["label"]["value"]

        # Otherwise, use the original language of the work
        elif "original language of work" in object:
            originalLanguageIds = set()

            for i, lang in enumerate(object["original language of work"]):
                languageLabel = lang

                if isinstance(lang, dict):
                    languageLabel = getItem(lang["value"])["label"] if lang["type"] == "item" else lang["value"]

                try:
                    originalLanguageIds.add(language.nameToIsoId(languageLabel))
                except KeyError:
                    if languageLabel == u'n/a (silent film)':
                        continue

                    fatal("Item '%s' has unknown original language '%s'"  % (object["label"],  languageLabel),
                        file=args["<data>"], line=lineNum)

            if len(originalLanguageIds & languages) == 0:
                try:
                    error("Item '%s' is in language '%s'" % (object["label"], ",".join(list(originalLanguageIds))))
                except UnicodeEncodeError:
                    try:
                        error("Item '%s' is in language '%s'" % (json.dumps(object["label"]), ",".join(list(originalLanguages))))
                    except UnicodeEncodeError:
                        error("Item '%s' is in language '%s'"
                            % (json.dumps(object["label"]), ",".join([json.dumps(language) for language in orginalLanguages])))
                continue

    # For each property; note: use extracted key to allow deletion.
    #
    for property in object.keys():
        if property in unwantedProperties:
            del object[property]
            continue

        # Non list members (description, label, id) don't contain references to other objects
        if not isinstance(object[property], list):
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

        if property in objectProperties:
            pass

    package["items"        ][object["id"]] = object
    package[args["<class>"]].append(object["id"])
    del object["id"]

package[args["<class>"]].sort(key=lambda id: package["items"][id]["label"])
print json.dumps(package, sort_keys=True, indent=4, separators=(',', ': '))
