#!/usr/bin/env python2.7

import malibu, sqlite3, unittest
from malibu.database import dbmapper
from nose.tools import *

class DBMapperTestCase(unittest.TestCase):

    def setUp(self):

        self.db = sqlite3.connect(":memory:")
    
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

    def recordLoad_test(self):

        dbm = DBMap(self.db)

        dbm.create()
        load_id = dbm.get_id()

        dbm.set_test_col("Test")
        dbm.set_example(True)
        dbm.set_description("This is a test.")
        dbm.save()
        
        del dbm

        dbm = DBMap(self.db)
        record = DBMap.load(id = load_id)

        self.assertEquals(record._test_col, "Test")
        self.assertEquals(record._example, True)
        self.assertEquals(record._description, "This is a test.")

class DBMap(dbmapper.DBMapper):

    def __init__(self, db):

        keys = ['id', 'test_col', 'example', 'description']
        ktypes = ['integer', 'text', 'boolean', 'text']

        DBMap.set_db_options(db, keys, ktypes)

        dbmapper.DBMapper.__init__(self, db, keys, ktypes)
