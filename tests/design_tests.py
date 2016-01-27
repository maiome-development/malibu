# -*- coding: utf-8 -*-
import contextlib, malibu, os, unittest, uuid
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


class Person(brine.BrineObject):

    def __init__(self):

        self.name = None
        super(Person, self).__init__(self, timestamp = True, uuid = True)


class PersonProfile(brine.BrineObject):

    def __init__(self):

        self.email = None
        self.person = Person()
        super(PersonProfile, self).__init__(self)


class UserProfile(brine.CachingBrineObject):

    def __init__(self):

        self.uuid = None
        self.timestamp = None
        self.user_id = None
        self.user_mail = None
        self.profile = PersonProfile()
        super(UserProfile, self).__init__(self, timestamp = False, uuid = False)


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

        self.assertEqual(aa.value, "abab")

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

        self.assertEqual(a.value, aa.value)


class BrineTestCase(unittest.TestCase):

    def brineInstanceCreate_test(self):

        a = Person()
        a.name = "John Smith"
        self.assertIsInstance(a, brine.BrineObject)
        self.assertIn("name", a.as_dict())
        self.assertEqual(a.as_dict()["name"], "John Smith")

    def brineNestedObject_test(self):

        a = Person()
        a.name = "John Smith"
        b = PersonProfile()
        b.email = "jsmith@example.org"

        def __reassign(*args, **kw):
            b.person = a

        self.assertRaises(
            AttributeError,
            __reassign,
            "object clobber")

        b.person.name = a.name
        a = b.person

        self.assertEqual(b.as_dict()["person"]["name"], a.name)

        a.name = "John Doe"

        self.assertEqual(b.as_dict()["person"]["name"], a.name)

    def brineInstanceFromJson_test(self):

        a = Person()
        a.name = "John Smith"
        js = a.to_json()

        b = Person.by_json(js)
        self.assertEqual(a.name, b.name)

    def brineInstanceFromDict_test(self):

        profile_data = {
            "email": "jdoe@example.org",
            "person": {
                "name": "John Doe",
            },
        }

        a = PersonProfile.by_dict(profile_data)

        self.assertEqual(a.email, "jdoe@example.org")
        self.assertEqual(a.person.name, "John Doe")

    def brineInstanceUseSpecialField_test(self):

        a = UserProfile()
        a.uuid = "custom-uuid-here"
        a.timestamp = "now"

        self.assertEqual(a.uuid, "custom-uuid-here")
        self.assertEqual(a.timestamp, "now")

        b = Person()
        try:
            b.uuid = "custom-uuid-here"
            b.timestamp = "now"
        except AttributeError as e:
            self.assertIsInstance(e, AttributeError)

    def cachingBrineInstanceFromDict_test(self):

        user_data = {
            "user_mail": "jdoe@example.org",
            "user_id": "jdoe214",
            "profile": {
                "email": "jdoe@example.org",
                "person": {
                    "name": "John Doe",
                },
            },
        }

        a = UserProfile.by_dict(user_data)

        self.assertEqual(a.user_mail, "jdoe@example.org")
        self.assertEqual(a.profile.email, "jdoe@example.org")
        self.assertEqual(a.profile.person.name, "John Doe")

    def cachingBrineSearch_test(self):

        person = Person()
        person.name = "John Doe"
        profile = UserProfile()
        profile.user_id = person.uuid
        profile.user_mail = "john.doe@example.com"

        a = UserProfile.search(user_id = person.uuid)

        self.assertGreaterEqual(len(a), 1)
        self.assertEqual(a[0].user_mail, "john.doe@example.com")
        self.assertEqual(a[0].user_id, person.uuid)

        a[0].uncache()

    def cachingBrineSearchUnready_test(self):

        class UnreadyTest(brine.CachingBrineObject):
            def __init__(self):
                self.val = None
                super(UnreadyTest, self).__init__(uuid=True)

        self.assertListEqual(UnreadyTest.search(val=""), [])

        u = UnreadyTest()
        u.val = "something"

        self.assertIn(u, UnreadyTest.search(val="something"))

    def cachingBrineFuzzySearch_test(self):

        self.skipTest("Fuzzy search is extremely broken. Needs more validation.")

        person = Person()
        person.name = "John Doe"
        profile = UserProfile()
        profile.user_id = person.uuid
        profile.user_mail = "john.doe@example.com"

        a = UserProfile.fuzzy_search(user_mail = "doe.john@example.org")

        self.assertGreaterEqual(len(a), 1)
        self.assertEqual(a[0].user_mail, "john.doe@example.com")
        self.assertEqual(a[0].user_id, person.uuid)

        a[0].uncache()

    def cachingBrineFuzzyRanking_test(self):

        Person().name = "John Doe"
        Person().name = "Jim Doe"
        Person().name = "Jane Doe"

        self.skipTest("Fuzzy search is extremely broken. Needs more validation.")

    def cachingBrineCreate_test(self):

        prof_a = UserProfile()
        self.assertIsInstance(prof_a, brine.CachingBrineObject)
        self.assertIn(prof_a, UserProfile._CachingBrineObject__cache)

        prof_a.uncache()

    def cachingBrineDirtyField_test(self):

        a = Person()
        a.name = "John Doe"

        prof_a = UserProfile()
        prof_a.user_id = a.uuid
        self.assertIn("user_id", prof_a._CachingBrineObject__dirty)

        ddump = prof_a.dirty_dict()
        self.assertIn("user_id", ddump)
        self.assertEqual(ddump["user_id"], a.uuid)

        prof_a.unmark("user_id")
        self.assertNotIn("user_id", prof_a.dirty_dict())
        self.assertIn("user_id", prof_a.as_dict())

        prof_a.uncache()
