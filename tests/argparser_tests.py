# -*- coding: utf-8 -*-
import contextlib, malibu, os, unittest
from malibu.util.args import ArgumentParser
from nose.tools import *


class ProxyObject(object):

    def __init__(self, ap):

        self.__ap = ap

    def get_ap(self):

        return self.__ap


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

    def argumentParserContextMgr_test(self):

        args = ['-c', 'filename.txt', '--syntax', 'plain', '-w']

        ap = ArgumentParser(args)
        pr = ProxyObject(ap)

        with pr.get_ap() as cap:
            cap.add_option_mapping('c', 'create')
            cap.add_option_type('create', opt = ArgumentParser.OPTION_PARAMETERIZED)
            cap.add_option_type('c', opt = ArgumentParser.OPTION_PARAMETERIZED)

            cap.add_option_type('syntax', opt = ArgumentParser.OPTION_PARAMETERIZED)

            cap.add_option_mapping('w', 'watch')

        ap.parse()

        self.assertEquals(ap.options['create'], 'filename.txt')
        self.assertEquals(ap.options['syntax'], 'plain')
        self.assertEquals(ap.options['watch'], True)
