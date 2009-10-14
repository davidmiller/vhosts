#!/usr/bin/env python
""" Test suite for localsite

Version 0.01
Author David Miller
"""
import unittest

from localsite import LocalSite

class MyTest(unittest.TestCase):

    def testTrue(self):
        myclass = LocalSite()

        try:
            result = myclass.retrieve()
            self.assertTrue(result)
        finally:
            pass
            

if __name__ == '__main__':
    unittest.main()
