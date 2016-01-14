# -*- coding: utf-8 -*-
from __future__ import print_function

import json
import unittest
from malibu.database import dbmapper
from nose.tools import *


class DBMapperTestCase(unittest.TestCase):

    def setUp(self):

        self.db = dbmapper.DBMapper.connect_database(":memory:")

    def tearDown(self):

        self.db.close()

    def recordCreate_test(self):

        dbm = DBMap(self.db)
        dbm.set_test_col("Test")
        dbm.set_example(True)
        dbm.set_description("This is a test.")

        self.assertEqual(dbm._test_col, "Test")
        self.assertEqual(dbm._example, True)
        self.assertEqual(dbm._description, "This is a test.")

    def recordDelete_test(self):

        dbm = DBMap(self.db)

        DBMap.new(test_col = "Test", example = False,
                description = "This could potentially be a test.")

        record = DBMap.find(test_col = "Test", example = False)

        self.assertNotEqual(len(record), 0)

        record = record[0]
        record.delete()

        record = DBMap.find(test_col = "Test", example = False)
        self.assertEqual(len(record), 0)

    def recordLoad_test(self):

        dbm = DBMap(self.db)

        dbm.create()
        load_id = dbm.get_id()

        dbm.set_test_col("Test")
        dbm.set_example(True)
        dbm.set_description("This is a test.")

        del dbm

        dbm = DBMap(self.db)
        record = DBMap.load(id = load_id)

        self.assertEqual(record._test_col, "Test")
        self.assertEqual(record._example, True)
        self.assertEqual(record._description, "This is a test.")

    def recordNew_test(self):

        dbm = DBMap(self.db)

        record = DBMap.new(test_col = "Test", example = False, description = "This is not a test.")

        self.assertEqual(record._test_col, "Test")
        self.assertEqual(record._example, False)
        self.assertEqual(record._description, "This is not a test.")

    def recordNewLoad_test(self):

        dbm = DBMap(self.db)

        record = DBMap.new(test_col = "Test", example = False, description = "This is not a test.")

        self.assertEqual(record._test_col, "Test")
        self.assertEqual(record._example, False)
        self.assertEqual(record._description, "This is not a test.")

        del record

        record = DBMap.load(test_col = "Test")

        self.assertEqual(record._test_col, "Test")
        self.assertEqual(record._example, False)
        self.assertEqual(record._description, "This is not a test.")

    def recordFind_test(self):

        dbm = DBMap(self.db)

        DBMap.new(test_col = "TestA", example = False, description = "This is not a test.")
        DBMap.new(test_col = "TestB", example = False, description = "This is still not a test.")

        result = DBMap.find(example = False)

        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]._test_col, "TestA")
        self.assertEqual(result[1]._test_col, "TestB")

    def recordFindAll_test(self):

        dbm = DBMap(self.db)

        DBMap.new(test_col = "TestA", example = False, description = "This is not a test.")
        DBMap.new(test_col = "TestB", example = False, description = "This is still not a test.")

        result = DBMap.find_all()

        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]._test_col, "TestA")
        self.assertEqual(result[1]._test_col, "TestB")

    def recordFilterEqual_test(self):

        dbm = DBMap(self.db)

        DBMap.new(test_col = "TestA", example = False, description = "This is not a test.")
        DBMap.new(test_col = "TestB", example = False, description = "This is still not a test.")

        result = DBMap.find_all()
        result = result.filter_equals("test_col", "TestA")

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]._test_col, "TestA")

    def recordFilterIequals_test(self):

        dbm = DBMap(self.db)

        DBMap.new(test_col = "TestA", example = False, description = "This is not a test.")
        DBMap.new(test_col = "TestB", example = False, description = "This is still not a test.")

        result = DBMap.find_all()
        result = result.filter_iequals("test_col", "testa")

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]._test_col, "TestA")

    def recordFilterInequals_test(self):

        dbm = DBMap(self.db)

        DBMap.new(test_col = "TestA", example = False, description = "This is not a test.")
        DBMap.new(test_col = "TestB", example = False, description = "This is still not a test.")

        result = DBMap.find_all()
        result = result.filter_inequals("test_col", "TestB")

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]._test_col, "TestA")

    def recordFilterRegex_test(self):

        dbm = DBMap(self.db)

        DBMap.new(test_col = "TestA", example = False, description = "This is not a test.")
        DBMap.new(test_col = "TestB", example = False, description = "This is still not a test.")

        result = DBMap.find_all()
        result = result.filter_regex("test_col", "Test[AB]")

        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]._test_col, "TestA")
        self.assertEqual(result[1]._test_col, "TestB")

    def recordJoin_test(self):

        dbm = DBMap(self.db)
        dbl = DBMapLink(self.db)

        DBMap.new(test_col = "TestA", example = False, description = "This is not a test.")
        DBMap.new(test_col = "TestB", example = False, description = "This is still not a test.")

        id_a = DBMap.load(test_col = "TestA").get_id()
        id_b = DBMap.load(test_col = "TestB").get_id()

        DBMapLink.new(map_id = id_a, some_text = "This definitely is not a test.")
        DBMapLink.new(map_id = id_b, some_text = "This might be a test.")
        DBMapLink.new(map_id = id_a, some_text = "This could be a test.")

        result = DBMap.join(DBMapLink, "id", "map_id")

        self.assertEqual(len(result), 2)
        self.assertEqual(result[0][0]._id, 1)
        self.assertEqual(result[0][1]._id, 2)
        self.assertEqual(result[1][0]._id, 1)
        self.assertEqual(result[1][1]._id, 2)

    def recordJoinFilter_test(self):

        dbm = DBMap(self.db)
        dbl = DBMapLink(self.db)

        DBMap.new(test_col = "TestA", example = False, description = "This is not a test.")
        DBMap.new(test_col = "TestB", example = False, description = "This is still not a test.")

        id_a = DBMap.load(test_col = "TestA").get_id()
        id_b = DBMap.load(test_col = "TestB").get_id()

        DBMapLink.new(map_id = id_a, some_text = "This definitely is not a test.")
        DBMapLink.new(map_id = id_b, some_text = "This might be a test.")
        DBMapLink.new(map_id = id_a, some_text = "This could be a test.")

        result = DBMap.join(DBMapLink, "id", "map_id")

        self.assertEqual(len(result), 2)
        self.assertEqual(len(result[0]), 3)
        self.assertEqual(len(result[1]), 3)

    def recordUniqueConstraint_test(self):

        dbo = DBMap(self.db)
        dbo = DBMapLink(self.db)

        DBMap.new(test_col = "TestA", example = False, description = "This is not a test.")
        DBMap.new(test_col = "TestB", example = False, description = "This is still not a test.")

        id_a = DBMap.load(test_col = "TestA").get_id()
        id_b = DBMap.load(test_col = "TestB").get_id()

        DBMapLink.new(map_id = id_a, some_text = "This definitely is not a test.", map_val = 'test')
        DBMapLink.new(map_id = id_b, some_text = "This might be a test.", map_val = 'notatest')

        self.assertRaises(dbmapper.DBMapperException, DBMapLink.new, **{'map_id' : id_a, 'some_text' : "This could be a test.", 'map_val' : 'test'})

    def recordJsonConv_test(self):

        self.skipTest("JSON conversion of output is broken.")

        dbo = DBMap(self.db)

        DBMap.new(test_col = "TestA", example = False, description = "This is not a test.", \
                stuff = json.dumps(['a', 'b', 'c']))

        obj_a = DBMap.load(test_col = "TestA")

        a_vals = obj_a.get_stuff()

        self.assertIsInstance(a_vals, list)
        self.assertListEqual(a_vals, ['a', 'b', 'c'])

    def recordSearch_test(self):

        dbo = DBMap(self.db)
        dbo = DBMapLink(self.db)

        DBMap.new(test_col = "TestA", example = False, description = "This is not a test.")
        DBMap.new(test_col = "TestB", example = False, description = "This is still not a test.")

        id_a = DBMap.load(test_col = "TestA").get_id()
        id_b = DBMap.load(test_col = "TestB").get_id()

        DBMapLink.new(map_id = id_a, some_text = "This definitely is not a test.", map_val = 'test')
        DBMapLink.new(map_id = id_b, some_text = "This might be a test.", map_val = 'notatest')

        matches = DBMap.search("Test")
        self.assertEqual(len(matches), 2)

        matches = DBMap.search("still")
        self.assertEqual(len(matches), 1)


class DBMap(dbmapper.DBMapper):

    def __init__(self, db):

        keys = ['id', 'test_col', 'example', 'description', 'stuff']
        ktypes = ['integer', 'text', 'boolean', 'text', 'json']

        options = DBMap.get_default_options()
        options[dbmapper.DBMapper.GENERATE_FTS_VT] = True

        DBMap.set_db_options(db, keys, ktypes, options = options)

        dbmapper.DBMapper.__init__(self, db, keys, ktypes, options = options)


class DBMapLink(dbmapper.DBMapper):

    def __init__(self, db):

        keys = ['id', 'map_id', 'some_text', 'map_val']
        ktypes = ['integer', 'integer', 'text', 'text']

        options = DBMapLink.get_default_options()
        options[dbmapper.DBMapper.INDEX_UNIQUE].add('map_val')

        DBMapLink.set_db_options(db, keys, ktypes, options = options)

        dbmapper.DBMapper.__init__(self, db, keys, ktypes, options = options)
