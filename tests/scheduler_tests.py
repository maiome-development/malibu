import contextlib, datetime, malibu
import os, time, unittest, uuid
from contextlib import closing
from datetime import datetime, timedelta
from malibu.util import scheduler
from nose.tools import *

class SchedulerTestCase(unittest.TestCase):

    def setUp(self):

        self.scheduler = scheduler.Scheduler()
        try:
            self.scheduler.save_state("testing")
        except NameError:
            self.scheduler.load_state("testing")
        self.result = []

    def __test_raise(self):

        raise Exception("Exception from scheduled function.")

    def schedulerStateCreation_test(self):

        test_func = lambda: True
        
        job = self.scheduler.create_job(
                name = "SchedulerTestCase__creationTest",
                func = test_func,
                delta = timedelta(seconds = 1),
                recurring = False)

        s = scheduler.Scheduler()
        s.load_state("testing")

        self.assertIn(job.get_name(), s._Scheduler__jobs)

        self.scheduler.remove_job(job.get_name())

        self.assertNotIn(job.get_name(), s._Scheduler__jobs)

    def schedulerJobTicking_test(self):

        test_id = uuid.uuid4()

        job = self.scheduler.create_job(
                name = "SchedulerTestCase__tickingTest",
                func = lambda: self.result.append(test_id),
                delta = timedelta(seconds = 1),
                recurring = False)

        time.sleep(1)

        self.assertTrue(job.is_ready(datetime.now()))
        self.scheduler.tick()
        self.assertEqual(self.result.pop(), test_id)

    def schedulerJobRaises_test(self):

        test_id = uuid.uuid4()

        job = self.scheduler.create_job(
                name = "SchedulerTestCase__raisesTest",
                func = self.__test_raise,
                delta = timedelta(seconds = 1),
                recurring = False)

        job.attach_onfail(lambda job: self.result.append(test_id))

        time.sleep(1)

        self.assertTrue(job.is_ready(datetime.now()))
        self.scheduler.tick()
        self.assertEqual(self.result.pop(), test_id)
