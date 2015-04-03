#!/usr/bin/env python2.7

import malibu, sqlite3, unittest, json
from malibu.database import dbmapper
from nose.tools import *
from sqlite3 import IntegrityError

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

        self.assertEquals(dbm._test_col, "Test")
        self.assertEquals(dbm._example, True)
        self.assertEquals(dbm._description, "This is a test.")

    def recordDelete_test(self):

        dbm = DBMap(self.db)

        DBMap.new(test_col = "Test", example = False, 
                description = "This could potentially be a test.")

        record = DBMap.find(test_col = "Test", example = False)

        self.assertNotEquals(len(record), 0)

        record = record[0]
        record.delete()

        record = DBMap.find(test_col = "Test", example = False)
        self.assertEquals(len(record), 0)

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

        self.assertEquals(record._test_col, "Test")
        self.assertEquals(record._example, True)
        self.assertEquals(record._description, "This is a test.")

    def recordNew_test(self):

        dbm = DBMap(self.db)

        record = DBMap.new(test_col = "Test", example = False, description = "This is not a test.")

        self.assertEquals(record._test_col, "Test")
        self.assertEquals(record._example, False)
        self.assertEquals(record._description, "This is not a test.")

    def recordNewLoad_test(self):

        dbm = DBMap(self.db)

        record = DBMap.new(test_col = "Test", example = False, description = "This is not a test.")

        self.assertEquals(record._test_col, "Test")
        self.assertEquals(record._example, False)
        self.assertEquals(record._description, "This is not a test.")

        del record

        record = DBMap.load(test_col = "Test")

        self.assertEquals(record._test_col, "Test")
        self.assertEquals(record._example, False)
        self.assertEquals(record._description, "This is not a test.")

    def recordFind_test(self):

        dbm = DBMap(self.db)

        DBMap.new(test_col = "TestA", example = False, description = "This is not a test.")
        DBMap.new(test_col = "TestB", example = False, description = "This is still not a test.")

        result = DBMap.find(example = False)
        
        self.assertEquals(len(result), 2)
        self.assertEquals(result[0]._test_col, "TestA")
        self.assertEquals(result[1]._test_col, "TestB")
    
    def recordFindAll_test(self):

        dbm = DBMap(self.db)

        DBMap.new(test_col = "TestA", example = False, description = "This is not a test.")
        DBMap.new(test_col = "TestB", example = False, description = "This is still not a test.")

        result = DBMap.find_all()
        
        self.assertEquals(len(result), 2)
        self.assertEquals(result[0]._test_col, "TestA")
        self.assertEquals(result[1]._test_col, "TestB")

    def recordFilterEquals_test(self):

        dbm = DBMap(self.db)

        DBMap.new(test_col = "TestA", example = False, description = "This is not a test.")
        DBMap.new(test_col = "TestB", example = False, description = "This is still not a test.")

        result = DBMap.find_all()
        result = result.filter_equals("test_col", "TestA")
        
        self.assertEquals(len(result), 1)
        self.assertEquals(result[0]._test_col, "TestA")

    def recordFilterIequals_test(self):

        dbm = DBMap(self.db)

        DBMap.new(test_col = "TestA", example = False, description = "This is not a test.")
        DBMap.new(test_col = "TestB", example = False, description = "This is still not a test.")

        result = DBMap.find_all()
        result = result.filter_iequals("test_col", "testa")
        
        self.assertEquals(len(result), 1)
        self.assertEquals(result[0]._test_col, "TestA")

    def recordFilterInequals_test(self):

        dbm = DBMap(self.db)

        DBMap.new(test_col = "TestA", example = False, description = "This is not a test.")
        DBMap.new(test_col = "TestB", example = False, description = "This is still not a test.")

        result = DBMap.find_all()
        result = result.filter_inequals("test_col", "TestB")
        
        self.assertEquals(len(result), 1)
        self.assertEquals(result[0]._test_col, "TestA")

    def recordFilterRegex_test(self):

        dbm = DBMap(self.db)

        DBMap.new(test_col = "TestA", example = False, description = "This is not a test.")
        DBMap.new(test_col = "TestB", example = False, description = "This is still not a test.")

        result = DBMap.find_all()
        result = result.filter_regex("test_col", "Test[AB]")
        
        self.assertEquals(len(result), 2)
        self.assertEquals(result[0]._test_col, "TestA")
        self.assertEquals(result[1]._test_col, "TestB")

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

        self.assertEquals(len(result), 2)
        self.assertEquals(result[0][0]._id, 1)
        self.assertEquals(result[0][1]._id, 2)
        self.assertEquals(result[1][0]._id, 1)
        self.assertEquals(result[1][1]._id, 2)
    
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

        self.assertEquals(len(result), 2)
        self.assertEquals(len(result[0]), 3)
        self.assertEquals(len(result[1]), 3)

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

        dbo = DBMap(self.db)
        
        DBMap.new(test_col = "TestA", example = False, description = "This is not a test.", \
                stuff = json.dumps(['a', 'b', 'c']))

        obj_a = DBMap.load(test_col = "TestA")

        a_vals = obj_a.get_stuff()

        self.assertIsInstance(a_vals, list)
        self.assertListEqual(a_vals, ['a', 'b', 'c'])

class DBMap(dbmapper.DBMapper):

    def __init__(self, db):

        keys = ['id', 'test_col', 'example', 'description', 'stuff']
        ktypes = ['integer', 'text', 'boolean', 'text', 'json']

        options = DBMap.get_default_options()
        
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
