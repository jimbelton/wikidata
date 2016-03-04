#!/usr/bin/python

"""wd-diagram.py - generate a class diagram from extracted classes

Usage: wd-diagram.py [-dfw] <wd-classes-json>

Options:
    -d --dot          Output the diagram in dot format (default: ascii)
    -f --failonerror  If present, exit if an error occurs
    -w --warning      Print warnings
"""

import json
import os
import sys

sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), "lib"))
from docopt  import docopt
from options import error, fatal, warn, options
args                     = docopt(__doc__, version='1.0')
options["ignore-errors"] = not args["--failonerror"]
options["warning"]       = args["--warning"]

classes  = json.load(open(args["<wd-classes-json>"]))
idEntity = None

def printSubtree(idRoot, parents=set(), indent=""):
    if idRoot in parents:
        error("Class '%s' contains a self reference" % idRoot)
        return

    parents.add(idRoot)
    root = classes[idRoot]

    if "subclasses" in root:
        subclasses = root["subclasses"]

        if len(subclasses) > 1:
            subclasses.sort()

            for idSubclass in subclasses[1:-1]:
                try:
                    print indent + " +-" + classes[idSubclass]["label"]
                except UnicodeEncodeError:
                    print indent + " +-" + json.dumps(classes[idSubclass]["label"])

                printSubtree(idSubclass, parents, indent + " | ")

        try:
            print indent + " +-" + classes[subclasses[-1]]["label"]
        except UnicodeEncodeError:
            print indent + " +-" + json.dumps(classes[subclasses[-1]]["label"])

        printSubtree(subclasses[-1], parents, indent + "   ")

    parents.remove(idRoot)

if args["--dot"]:
    print "digraph classes {"

for idRight in classes:
    try:
        labelRight = classes[idRight]["label"]

        if labelRight == "entity":
            idEntity = idRight

    except KeyError:
        labelRight = idRight

    for idLeft in classes[idRight]["subclass of"]:
        if not args["--dot"]:
            try:
                if "subclasses" in classes[idLeft]:
                    classes[idLeft]["subclasses"].append(idRight)
                else:
                    classes[idLeft]["subclasses"] = [idRight]
            except (KeyError, TypeError):
                warn("Class '%s' is a subclass of '%s', which is not a class" % (labelRight, idLeft))

        else:
            try:
                labelLeft = classes[idLeft]["label"]
            except KeyError:
                labelLeft = idLeft
            except TypeError:
                warn("Class '%s' is a subclass of '%s', which is not a class" % (labelRight, idLeft))
                continue

            try:
                print '"%s" -> "%s"' % (labelRight, labelLeft)
            except UnicodeEncodeError:
                print '%s -> %s' % (json.dumps(labelRight), json.dumps(labelLeft))

if args["--dot"]:
    print "}"
    sys.exit(0)

if idEntity == None:
    fatal("Root class 'entity' was not found")

print classes[idEntity]["label"]
printSubtree(idEntity)
