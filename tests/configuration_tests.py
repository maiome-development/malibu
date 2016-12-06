# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from __future__ import print_function

import io
import os
import unittest

from malibu.config.configuration import Configuration
from malibu.text import str2unicode, unicode_type
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

            self.assertEqual(main.get_string('a'), 'b')
            self.assertEqual(main.get_int('b'), 2)
            self.assertIsInstance(main.get('c'), unicode_type())
            self.assertIsInstance(main.get('d'), dict)
            self.assertIsNone(main.get('e', object()))

            self.assertEqual(test.get('e'), 'test e')
            self.assertEqual(test.get_bool('f'), True)
            self.assertListEqual(test.get_list('g'), ['list', 'of', 'things'])
            self.assertIsInstance(test.get('h'), list)
            self.assertListEqual(test.get('h'), [b'list', b'of', b'things'])

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

            l1 = test.get_list('g', default=None)
            self.assertEqual(l1, ['list', 'of', 'things'])

            l2 = str2unicode(test.get_list('h', default=None))
            self.assertEqual(l2, [b'list', b'of', b'things'])

    def configSectionNamespace_test(self):

        with io.open(self.config_path, 'r') as config_fobj:
            self.config.load_file(config_fobj)
            self.assertTrue(self.config.loaded)

            namespaced = self.config.get_namespace('ns')
            self.assertEqual(len(namespaced), 2)

            for name, section in namespaced.items():
                self.assertIsNotNone(section)
                self.assertIn(name, ["first", "second"])
                self.assertIn(section.get_int("value"), [1, 2])

    def configSectionLinkedNamespace_test(self):

        with io.open(self.config_path, 'r') as config_fobj:
            self.config.load_file(config_fobj)
            self.assertTrue(self.config.loaded)

            scheduler_conf = self.config.get_section("scheduler")
            jobstore_conf = scheduler_conf.get("job_store", None)
            self.assertIsNotNone(jobstore_conf)

            self.assertEquals(jobstore_conf.get_string("type", "volatile"), "testing-volatile")
