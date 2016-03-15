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

        self.assertEqual(ap.options['create'], True)

    def argumentParserParameterized_test(self):

        args = ['-c', 'filename.txt']

        ap = ArgumentParser(args, mapping = {'c' : 'create'})
        ap.add_option_type('c', opt = ArgumentParser.OPTION_PARAMETERIZED)
        ap.parse()

        self.assertEqual(ap.options['create'], 'filename.txt')

    def argumentParserMultiple_test(self):

        args = ['-c', 'filename.txt', '--syntax', 'plain', '-w']

        ap = ArgumentParser(args)
        ap.add_option_mapping('c', 'create')
        ap.add_option_type('c', opt = ArgumentParser.OPTION_PARAMETERIZED)

        ap.add_option_type('syntax', opt = ArgumentParser.OPTION_PARAMETERIZED)

        ap.add_option_mapping('w', 'watch')
        ap.parse()

        self.assertEqual(ap.options['create'], 'filename.txt')
        self.assertEqual(ap.options['syntax'], 'plain')
        self.assertEqual(ap.options['watch'], True)

    def argumentParserDashedParms_test(self):

        args = ['--target', '-19000000', '--message', 'Test']

        ap = ArgumentParser(args)
        ap.add_option_type('target', opt = ArgumentParser.OPTION_PARAMETERIZED)
        ap.add_option_type('message', opt = ArgumentParser.OPTION_PARAMETERIZED)

        ap.parse()

        self.assertEqual(ap.options['target'], '-19000000')
        self.assertEqual(ap.options['message'], 'Test')

    def argumentParserQuotedDashedParms_test(self):

        args = ['--target', '"-19000000"', '--message', 'Test']

        ap = ArgumentParser(args)
        ap.add_option_type('target', opt = ArgumentParser.OPTION_PARAMETERIZED)
        ap.add_option_type('message', opt = ArgumentParser.OPTION_PARAMETERIZED)

        ap.parse()

        self.assertEqual(ap.options['target'], '-19000000')
        self.assertEqual(ap.options['message'], 'Test')

    def argumentParserQuotedParms_test(self):

        args = ['--target', '"-19000000"', '--message', "'Test'",
                '--file', '"unmatched.txt', '--syntax=plain']

        ap = ArgumentParser(args)
        ap.add_option_type('target', opt = ArgumentParser.OPTION_PARAMETERIZED)
        ap.add_option_type('message', opt = ArgumentParser.OPTION_PARAMETERIZED)
        ap.add_option_type('file', opt = ArgumentParser.OPTION_PARAMETERIZED)
        ap.add_option_type('syntax', opt = ArgumentParser.OPTION_PARAMETERIZED)

        ap.parse()

        self.assertEqual(ap.options['target'], '-19000000')
        self.assertEqual(ap.options['message'], 'Test')
        self.assertEqual(ap.options['file'], 'unmatched.txt')
        self.assertEqual(ap.options['syntax'], 'plain')

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

        self.assertEqual(ap.options['create'], 'filename.txt')
        self.assertEqual(ap.options['syntax'], 'plain')
        self.assertEqual(ap.options['watch'], True)
