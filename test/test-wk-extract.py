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
        linesOut = open(os.path.join(wikidataDir, "test/1000.out")).read().split()
        linesNew = subprocess.check_output([wdExtractPy, "-f", "-l", "en", "-s", "", os.path.join(wikidataDir, "data/1000.json")]).split()
        diff     = list(difflib.Differ().compare(linesOut, linesNew))
        self.assertEqual(len(diff), 0, "Unexpected differences in output of wd-extract.py -f -l en -s '' data/1000.json\n" + "".join(diff))

if __name__ == '__main__':
    unittest.main()
