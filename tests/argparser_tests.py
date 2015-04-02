#!/usr/bin/env python2.7

import contextlib, malibu, os, unittest
from malibu.util.args import ArgumentParser
from nose.tools import *

class ArgumentParserTestCase(unittest.TestCase):

    def argumentParserSingle_test(self):

        args = ['-c']

        ap = ArgumentParser(args, mapping = {'c' : 'create'})
        ap.parse()

        self.assertEquals(ap.options['create'], True)

    def argumentParserParameterized_test(self):

        args = ['-c', 'filename.txt']

        ap = ArgumentParser(args, mapping = {'c' : 'create'})
        ap.add_option_type('c', opt = ArgumentParser.OPTION_PARAMETERIZED)
        ap.parse()

        self.assertEquals(ap.options['create'], 'filename.txt')

    def argumentParserMultiple_test(self):

        args = ['-c', 'filename.txt', '--syntax', 'plain', '-w']

        ap = ArgumentParser(args)
        ap.add_option_mapping('c', 'create')
        ap.add_option_type('c', opt = ArgumentParser.OPTION_PARAMETERIZED)

        ap.add_option_type('syntax', opt = ArgumentParser.OPTION_PARAMETERIZED)

        ap.add_option_mapping('w', 'watch')
        ap.parse()

        self.assertEquals(ap.options['create'], 'filename.txt')
        self.assertEquals(ap.options['syntax'], 'plain')
        self.assertEquals(ap.options['watch'], True)
