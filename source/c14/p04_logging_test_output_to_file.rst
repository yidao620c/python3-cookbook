==============================
14.4 将测试输出用日志记录到文件中
==============================

----------
问题
----------
You want the results of running unit tests written to a file instead of printed to standard
output.

Solution
A very common technique for running unit tests is to include a small code fragment
like this at the bottom of your testing file:

import unittest

class MyTest(unittest.TestCase):
    ...

if __name__ == '__main__':
    unittest.main()

This makes the test file executable, and prints the results of running tests to standard
output. If you would like to redirect this output, you need to unwind the main() call a
bit and write your own main() function like this:

import sys
def main(out=sys.stderr, verbosity=2):
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromModule(sys.modules[__name__])
    unittest.TextTestRunner(out,verbosity=verbosity).run(suite)

if __name__ == '__main__':
    with open('testing.out', 'w') as f:
        main(f)

Discussion
The interesting thing about this recipe is not so much the task of getting test results
redirected to a file, but the fact that doing so exposes some notable inner workings of
the unittest module.
At a basic level, the unittest module works by first assembling a test suite. This test
suite consists of the different testing methods you defined. Once the suite has been
assembled, the tests it contains are executed.

These two parts of unit testing are separate from each other. The unittest.TestLoad
er instance created in the solution is used to assemble a test suite. The loadTestsFrom
Module() is one of several methods it defines to gather tests. In this case, it scans a
module for TestCase classes and extracts test methods from them. If you want some‐
thing more fine-grained, the loadTestsFromTestCase() method (not shown) can be
used to pull test methods from an individual class that inherits from TestCase.
The TextTestRunner class is an example of a test runner class. The main purpose of
this class is to execute the tests contained in a test suite. This class is the same test runner
that sits behind the unittest.main() function. However, here we’re giving it a bit of
low-level configuration, including an output file and an elevated verbosity level.
Although this recipe only consists of a few lines of code, it gives a hint as to how you
might further customize the  unittest framework. To customize how test suites are
assembled, you would perform various operations using the TestLoader class. To cus‐
tomize how tests execute, you could make custom test runner classes that emulate the
functionality of TextTestRunner. Both topics are beyond the scope of what can be cov‐
ered here. However, documentation for the unittest module has extensive coverage
of the underlying protocols. 
