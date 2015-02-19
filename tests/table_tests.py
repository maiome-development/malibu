#!/usr/bin/env python2.7

import malibu, sqlite3, unittest
from malibu.text.table import TextTable
from nose.tools import *
from sqlite3 import IntegrityError

class TableTestCase(unittest.TestCase):

    def setUp(self):

        self.x = ['a', 'b', 'c', 'd']
        self.y = ['e', 'f', 'g', 'h']
        self.z = ['i', 'j', 'k', 'l']

        self.table = TextTable()

    def ztupAdd_test(self):

        result = \
"""+------------+------------+------------+
|          x |          y |          z |
+------------+------------+------------+
|          a |          e |          i |
|          b |          f |          j |
|          c |          g |          k |
|          d |          h |          l |
+------------+------------+------------+
"""

        self.table.add_header(*['x', 'y', 'z'])
        self.table.add_data_ztup(zip(self.x, self.y, self.z))

        s = ""
        for line in self.table.format():
            s += line + "\n"

        self.assertEquals(s, result)
