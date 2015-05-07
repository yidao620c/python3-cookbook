===============================
14.3 在单元测试中测试异常情况
===============================

----------
问题
----------
You want to write a unit test that cleanly tests if an exception is raised.

|

----------
解决方案
----------
To test for exceptions, use the assertRaises() method. For example, if you want to test
that a function raised a ValueError exception, use this code:

import unittest

# A simple function to illustrate
def parse_int(s):
    return int(s)

class TestConversion(unittest.TestCase):
    def test_bad_int(self):
        self.assertRaises(ValueError, parse_int, 'N/A')

If you need to test the exception’s value in some way, then a different approach is needed.
For example:

import errno

class TestIO(unittest.TestCase):
    def test_file_not_found(self):
        try:
            f = open('/file/not/found')
        except IOError as e:
            self.assertEqual(e.errno, errno.ENOENT)

        else:
            self.fail('IOError not raised')

|

----------
讨论
----------
The assertRaises() method provides a convenient way to test for the presence of an
exception. A common pitfall is to write tests that manually try to do things with excep‐
tions on their own. For instance:

class TestConversion(unittest.TestCase):
    def test_bad_int(self):
        try:
            r = parse_int('N/A')
        except ValueError as e:
            self.assertEqual(type(e), ValueError)

The problem with such approaches is that it is easy to forget about corner cases, such
as that when no exception is raised at all. To do that, you need to add an extra check for
that situation, as shown here:

class TestConversion(unittest.TestCase):
    def test_bad_int(self):
        try:
            r = parse_int('N/A')
        except ValueError as e:
            self.assertEqual(type(e), ValueError)
        else:
            self.fail('ValueError not raised')

The assertRaises() method simply takes care of these details, so you should prefer to
use it.
The one limitation of assertRaises() is that it doesn’t provide a means for testing the
value of the exception object that’s created. To do that, you have to manually test it, as
shown. Somewhere in between these two extremes, you might consider using the as
sertRaisesRegex() method, which allows you to test for an exception and perform a
regular expression match against the exception’s string representation at the same time.
For example:

class TestConversion(unittest.TestCase):
    def test_bad_int(self):
        self.assertRaisesRegex(ValueError, 'invalid literal .*',
                                       parse_int, 'N/A')

A little-known fact about assertRaises() and assertRaisesRegex() is that they can
also be used as context managers:

class TestConversion(unittest.TestCase):
    def test_bad_int(self):
        with self.assertRaisesRegex(ValueError, 'invalid literal .*'):
            r = parse_int('N/A')

This form can be useful if your test involves multiple steps (e.g., setup) besides that of
simply executing a callable.
