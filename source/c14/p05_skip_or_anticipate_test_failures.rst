==============================
14.5 忽略或者期望测试失败
==============================

----------
问题
----------
You want to skip or mark selected tests as an anticipated failure in your unit tests.

Solution
The unittest module has decorators that can be applied to selected test methods to
control their handling. For example:

import unittest
import os
import platform

class Tests(unittest.TestCase):
    def test_0(self):
        self.assertTrue(True)

    @unittest.skip('skipped test')
    def test_1(self):
        self.fail('should have failed!')

    @unittest.skipIf(os.name=='posix', 'Not supported on Unix')
    def test_2(self):
        import winreg

    @unittest.skipUnless(platform.system() == 'Darwin', 'Mac specific test')
    def test_3(self):
        self.assertTrue(True)

    @unittest.expectedFailure
    def test_4(self):
        self.assertEqual(2+2, 5)

if __name__ == '__main__':
    unittest.main()

If you run this code on a Mac, you’ll get this output:

    bash % python3 testsample.py -v
    test_0 (__main__.Tests) ... ok
    test_1 (__main__.Tests) ... skipped 'skipped test'
    test_2 (__main__.Tests) ... skipped 'Not supported on Unix'
    test_3 (__main__.Tests) ... ok
    test_4 (__main__.Tests) ... expected failure

    ----------------------------------------------------------------------
    Ran 5 tests in 0.002s

    OK (skipped=2, expected failures=1)

Discussion
The skip() decorator can be used to skip over a test that you don’t want to run at all.
skipIf() and skipUnless() can be a useful way to write tests that only apply to certain
platforms or Python versions, or which have other dependencies. Use the @expected
Failure decorator to mark tests that are known failures, but for which you don’t want
the test framework to report more information.
The decorators for skipping methods can also be applied to entire testing classes. For
example:

@unittest.skipUnless(platform.system() == 'Darwin', 'Mac specific tests')
class DarwinTests(unittest.TestCase):
    ...

