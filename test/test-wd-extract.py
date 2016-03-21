#!/usr/bin/python

import difflib
import os
import sys
import subprocess
import unittest

wikidataDir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
wdExtractPy = os.path.join(wikidataDir, "wd-extract.py")

class TestWkExtract(unittest.TestCase):
    def testSimplify(self):
        inputFile = os.path.join(wikidataDir, "data/1000.json")
        linesOut  = open(os.path.join(wikidataDir, "test/1000.out")).read().split()
        linesNew  = subprocess.check_output([wdExtractPy, "-f", "-F", "-l", "en", "-s", "", "-t", "all", inputFile]).split()
        diff      = list(difflib.context_diff(linesOut, linesNew))
        self.assertEqual(len(diff), 0, "Unexpected differences in output of wd-extract.py -f -F -l en -s '' -t all data/1000.json\n"
                                       + "".join(diff))

if __name__ == '__main__':
    unittest.main()
