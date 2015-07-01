import contextlib, malibu, os, unittest
from contextlib import closing
from malibu.design import borgish
from nose.tools import *


class ClassA(borgish.SharedState):

    def __init__(self, *args, **kw):

        super(ClassA, self).__init__(self, *args, **kw)
        self.value = "aaaa"


class ClassB(borgish.SharedState):

    def __init__(self, *args, **kw):

        super(ClassB, self).__init__(self, *args, **kw)
        self.value = "bbbb"


class BorgishTestCase(unittest.TestCase):

    def borgishInstanceCreate_test(self):

        a = ClassA()
        self.assertIsInstance(a, borgish.SharedState)

    def borgishSaveState_test(self):

        a = ClassA()
        a.save_state("save")

        self.assertIn("save", a._SharedState__states)

    def borgishStateLoad_test(self):

        a = ClassA()
        a.value = "abab"
        a.save_state("load")

        aa = ClassA()
        aa.load_state("load")

        self.assertEquals(aa.value, "abab")

    def borgishStateOverwrite_test(self):

        a = ClassA()
        a.value = "abab"
        a.save_state("overwrite")

        aa = ClassA()
        aa.value = "baba"

        self.assertRaises(NameError, aa.save_state, "overwrite")

    def borgishClassesDisjoint_test(self):

        a = ClassA()
        a.value = "abab"
        a.save_state("disjoint")

        b = ClassB()

        self.assertRaises(NameError, b.load_state, "disjoint")

    def borgishStateCarry_test(self):

        a = ClassA()
        a.save_state("carry")
        a.value = "abab"

        aa = ClassA()
        aa.load_state("carry")

        self.assertEquals(a.value, aa.value)
