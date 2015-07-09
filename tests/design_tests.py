import contextlib, malibu, os, unittest
from contextlib import closing
from malibu.design import borgish
from malibu.design import brine
from nose.tools import *


class ClassA(borgish.SharedState):

    def __init__(self, *args, **kw):

        super(ClassA, self).__init__(self, *args, **kw)
        self.value = "aaaa"


class ClassB(borgish.SharedState):

    def __init__(self, *args, **kw):

        super(ClassB, self).__init__(self, *args, **kw)
        self.value = "bbbb"


class Person(brine.BrineState):

    def __init__(self):

        self.name = None
        super(Person, self).__init__(self, timestamp = True, uuid = True)


class UserProfile(brine.CachingBrineState):

    def __init__(self):

        self.user_id = None
        self.user_mail = None
        super(UserProfile, self).__init__(self, timestamp = True, uuid = True)


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


class BrineTestCase(unittest.TestCase):

    def brineInstanceCreate_test(self):

        a = Person()
        self.assertIsInstance(a, brine.BrineState)
        self.assertIn(a, Person._BrineState__cache)
        
        a.uncache()

    def brineSearch_test(self):

        Person().name = "John Doe"
        
        a = Person.search(name = "John Doe")

        self.assertGreaterEqual(len(a), 1)
        self.assertEqual(a[0].name, "John Doe")

        a[0].uncache()

    def brineFuzzySearch_test(self):

        Person().name = "John Doe"

        self.skipTest("Fuzzy search is extremely broken. Needs more validation.")
        
        a = Person.fuzzy_search(name = "Doe John")

        self.assertGreaterEqual(len(a), 1)
        self.assertEqual(a[0].name, "John Doe")

        a[0].uncache()

    def brineFuzzyRanking_test(self):

        Person().name = "John Doe"
        Person().name = "Jim Doe"
        Person().name = "Jane Doe"

        self.skipTest("Fuzzy search is extremely broken. Needs more validation.")

    def cachingBrineCreate_test(self):

        prof_a = UserProfile()
        self.assertIsInstance(prof_a, brine.CachingBrineState)
        self.assertIn(prof_a, UserProfile._BrineState__cache)

        prof_a.uncache()

    def cachingBrineDirtyField_test(self):

        a = Person()
        a.name = "John Doe"

        self.skipTest("Cache dirtying is currently broken.")
        
        prof_a = UserProfile()
        prof_a.user_id = a.uuid
        self.assertIn("user_id", prof_a._CachingBrineState__dirty)

        ddump = prof_a.as_dict()
        self.assertIn("user_id", ddump)
        self.assertEquals(ddump["uuid"], a.uuid)
