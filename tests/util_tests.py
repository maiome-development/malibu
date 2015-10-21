import contextlib, datetime, malibu
import os, time, unittest
from malibu import util
from malibu.util import decorators
from nose.tools import *


class UtilTestCase(unittest.TestCase):

    def setUp(self):

        self._target = []
        self.func_regis = decorators.function_registrator(self._target)
        self.func_mark = decorators.function_marker("f_type", "testing")

    def return_caller(self):

        return util.get_caller()

    def return_frame(self):

        return util.get_calling_frame()

    def callerReturn_test(self):

        self.assertEquals(self.return_caller(), "tests.util_tests.UtilTestCase.callerReturn_test")

    def callerFrame_test(self):

        frame = self.return_frame()
        self.assertEquals(frame.f_code.co_name, "callerFrame_test")

    def currentReturn_test(self):

        self.assertEquals(util.get_current(), "tests.util_tests.UtilTestCase.currentReturn_test")

    def currentFrame_test(self):

        frame = util.get_current_frame()
        self.assertEquals(frame.f_code.co_name, "currentFrame_test")

    def decorFunctionRegistrator_test(self):

        @self.func_regis
        def does_nothing():
            pass

        self.assertIn(does_nothing, self._target)

    def decorFunctionMarker_test(self):

        @self.func_mark
        def does_nothing():
            pass

        self.assertNotEquals(getattr(does_nothing, "f_type", None), None)
        self.assertEquals(does_nothing.f_type, "testing")

    def decorRegistratorMarkerStackable_test(self):

        @self.func_mark
        @self.func_regis
        def does_nothing():
            pass

        self.assertNotEquals(getattr(does_nothing, "f_type", None), None)
        self.assertEquals(does_nothing.f_type, "testing")
        self.assertIn(does_nothing, self._target)

