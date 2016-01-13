#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

import contextlib, io, malibu, os, unittest
from contextlib import closing
from malibu.config.configuration import Configuration
from nose.tools import *


class ConfigurationTestCase(unittest.TestCase):

    def setUp(self):

        self.config = Configuration()
        self.config_path = os.getcwd() + "/tests/config.txt"

    def configLoad_test(self):

        self.config.load(self.config_path)
        self.assertTrue(self.config.loaded)

    def configLoadFile_test(self):

        with io.open(self.config_path, 'r') as config_fobj:
            self.config.load_file(config_fobj)
            self.assertTrue(self.config.loaded)

    def configSectionGetValues_test(self):

        with io.open(self.config_path, 'r') as config_fobj:
            self.config.load_file(config_fobj)
            self.assertTrue(self.config.loaded)

            main = self.config.get_section('main')
            test = self.config.get_section('test')
            self.assertIsNot(main, None)
            self.assertIsNot(test, None)

            self.assertEquals(main.get_string('a'), 'b')
            self.assertEquals(main.get_int('b'), 2)
            self.assertIsInstance(main.get('c'), unicode)
            self.assertIsInstance(main.get('d'), dict)

            self.assertEquals(test.get('e'), 'test e')
            self.assertEquals(test.get_bool('f'), True)
            self.assertListEqual(test.get_list('g'), ['list', 'of', 'things'])
            self.assertIsInstance(test.get('h'), list)
            self.assertListEqual(test.get('h'), [u'list', u'of', u'things'])

    def configSections_test(self):

        with io.open(self.config_path, 'r') as config_fobj:
            self.config.load_file(config_fobj)
            self.assertTrue(self.config.loaded)

            self.assertIn("main", self.config.sections)
            self.assertIn("test", self.config.sections)

    def configSectionGetList_test(self):

        with io.open(self.config_path, 'r') as config_fobj:
            self.config.load_file(config_fobj)
            self.assertTrue(self.config.loaded)

            test = self.config.get_section('test')
            self.assertIsNot(test, None)

            l1 = test.get_list('g', default = None)
            self.assertEquals(l1, ['list', 'of', 'things'])

            l2 = test.get_list('h', default = None)
            self.assertEquals(l2, ['list', 'of', 'things'])
