#!/usr/bin/python

import os
import sys
import unittest

sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), "../lib"))
import simplify

class TestSimplify(unittest.TestCase):
    def testTimeToDate(self):
        date = simplify.time(
            {
                "type": "time",
                "value": {
                    "after": 0,
                    "before": 0,
                    "calendarmodel": "http://www.wikidata.org/entity/Q1985727",
                    "precision": 10,    # Accurate to the month
                    "time": "+1942-10-00T00:00:00Z",
                    "timezone": 0
                }
            }
        )

        self.assertEqual(len(date.keys()), 3)
        self.assertEqual(date["type"],      "date")
        self.assertEqual(date["value"],     "1942-10-00")
        self.assertEqual(date["precision"], 10)

if __name__ == '__main__':
    unittest.main()
