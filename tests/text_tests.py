# -*- coding: utf-8 -*-
import sys
import unittest

from malibu.text import (
    str2unicode,
    unicode2str,
)
from nose.tools import *
from sqlite3 import IntegrityError


class StrconvTestCase(unittest.TestCase):

    def py3Setup(self):

        self.a = "unicode str"
        self.b = b"bytes str"

    def py2Setup(self):

        self.a = "regular str"
        self.b = u"unicode str"

    def py2Strconv_test(self):

        if sys.version_info.major != 2:
            self.skipTest("This test only runs on Python 2.")

        self.py2Setup()

        a = unicode2str(self.a)
        b = unicode2str(self.b)

        self.assertEqual(a, self.a)
        self.assertEqual(b, "unicode str")
        self.assertTrue(isinstance(a, str))
        self.assertTrue(isinstance(b, str))

        a = str2unicode(self.a)
        b = str2unicode(self.b)

        self.assertEqual(a, u"regular str")
        self.assertEqual(b, self.b)
        self.assertTrue(isinstance(a, unicode))
        self.assertTrue(isinstance(b, unicode))

    def py3Strconv_test(self):

        if sys.version_info.major != 3:
            self.skipTest("This test only runs on Python 3.")

        self.py3Setup()

        a = unicode2str(self.a)
        b = unicode2str(self.b)

        self.assertEqual(a, b"unicode str")
        self.assertEqual(b, self.b)
        self.assertTrue(isinstance(a, bytes))
        self.assertTrue(isinstance(b, bytes))

        a = str2unicode(self.a)
        b = str2unicode(self.b)

        self.assertEqual(a, self.a)
        self.assertEqual(b, "bytes str")
        self.assertTrue(isinstance(a, str))
        self.assertTrue(isinstance(b, str))

