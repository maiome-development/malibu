# -*- coding: utf-8 -*-
import unittest

from malibu import util
from malibu.util import decorators
from nose.tools import *


class UtilTestCase(unittest.TestCase):

    def setUp(self):

        self._target = []
        self._d_target = {}
        self.func_regis = decorators.function_registrator(self._target)
        self.func_mark = decorators.function_marker("f_type", "testing")
        self.func_kw_reg = decorators.function_kw_reg(self._d_target, ["deps"])

    def return_caller(self):

        return util.get_caller()

    def return_frame(self):

        return util.get_calling_frame()

    def callerReturn_test(self):

        self.assertEqual(self.return_caller(), "tests.util_tests.UtilTestCase.callerReturn_test")

    def callerFrame_test(self):

        frame = self.return_frame()
        self.assertEqual(frame.f_code.co_name, "callerFrame_test")

    def currentReturn_test(self):

        self.assertEqual(util.get_current(), "tests.util_tests.UtilTestCase.currentReturn_test")

    def currentFrame_test(self):

        frame = util.get_current_frame()
        self.assertEqual(frame.f_code.co_name, "currentFrame_test")

    def decorFunctionRegistrator_test(self):

        @self.func_regis
        def does_nothing():
            pass

        self.assertIn(does_nothing, self._target)

    def decorFunctionMarker_test(self):

        @self.func_mark
        def does_nothing():
            pass

        self.assertNotEqual(getattr(does_nothing, "f_type", None), None)
        self.assertEqual(does_nothing.f_type, "testing")

    def decorRegistratorMarkerStackable_test(self):

        @self.func_mark
        @self.func_regis
        def does_nothing():
            pass

        self.assertNotEqual(getattr(does_nothing, "f_type", None), None)
        self.assertEqual(does_nothing.f_type, "testing")
        self.assertIn(does_nothing, self._target)

    def decorWrappable_test(self):

        def func_mark(func):
            self.func_mark(func)
            self.func_regis(func)

            return func

        @func_mark
        def does_nothing():
            pass

        self.assertNotEqual(getattr(does_nothing, "f_type", None), None)
        self.assertEqual(does_nothing.f_type, "testing")
        self.assertIn(does_nothing, self._target)

    def decorKwReg_test(self):

        try:
            @self.func_kw_reg(loads=['test'])
            def just_fails():
                pass
        except Exception as e:
            self.assertIsInstance(e, KeyError)

        try:
            @self.func_kw_reg(deps=['test'])
            def just_works():
                return True
            self.assertTrue(just_works())
        except Exception as e:
            self.fail("This section of the test should not have failed.")

    def decorInterceptor_test(self):

        def _intercept_func_stuff(*args, **kw):

            if 'thing' in kw:
                return {'thing': True}
            else:
                return {'thing': None}

        func_interceptor = decorators.function_intercept_scope(
            _intercept_func_stuff,
            intercept_args=True)

        @func_interceptor
        def does_stuff(*args, **kw):

            global thing

            try:
                thing = thing if thing else None
            except:
                self.fail("Injected value did not appear")

            self.assertEqual(thing, True)
            return True

        retv = does_stuff(thing="hello")
        self.assertTrue(retv)
