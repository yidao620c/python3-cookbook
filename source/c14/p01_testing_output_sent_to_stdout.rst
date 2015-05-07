==============================
14.1 测试输出到标准输出上
==============================

----------
问题
----------
You  have  a  program  that  has  a  method  whose  output  goes  to  standard  Output
(sys.stdout). This almost always means that it emits text to the screen. You’d like to
write a test for your code to prove that, given the proper input, the proper output is
displayed.

|

----------
解决方案
----------
Using the unittest.mock module’s patch() function, it’s pretty simple to mock out
sys.stdout for just a single test, and put it back again, without messy temporary vari‐
ables or leaking mocked-out state between test cases.
Consider, as an example, the following function in a module mymodule:

# mymodule.py

def urlprint(protocol, host, domain):
    url = '{}://{}.{}'.format(protocol, host, domain)
    print(url)

The built-in print function, by default, sends output to sys.stdout. In order to test
that output is actually getting there, you can mock it out using a stand-in object, and
then make assertions about what happened. Using the unittest.mock module’s patch()
method makes it convenient to replace objects only within the context of a running test,
returning things to their original state immediately after the test is complete. Here’s the
test code for mymodule:

from io import StringIO
from unittest import TestCase
from unittest.mock import patch
import mymodule

class TestURLPrint(TestCase):
    def test_url_gets_to_stdout(self):
        protocol = 'http'
        host = 'www'
        domain = 'example.com'
        expected_url = '{}://{}.{}\n'.format(protocol, host, domain)

        with patch('sys.stdout', new=StringIO()) as fake_out:
            mymodule.urlprint(protocol, host, domain)
            self.assertEqual(fake_out.getvalue(), expected_url)

|

----------
讨论
----------
The urlprint() function takes three arguments, and the test starts by setting up dummy
arguments for each one. The expected_url variable is set to a string containing the
expected output.
To run the test, the unittest.mock.patch() function is used as a context manager to
replace the value of sys.stdout with a StringIO object as a substitute. The fake_out
variable is the mock object that’s created in this process. This can be used inside the
body of the with statement to perform various checks. When the with statement com‐
pletes, patch conveniently puts everything back the way it was before the test ever ran.
It’s worth noting that certain C extensions to Python may write directly to standard
output, bypassing the setting of sys.stdout. This recipe won’t help with that scenario,
but it should work fine with pure Python code (if you need to capture I/O from such C
extensions, you can do it by opening a temporary file and performing various tricks
involving file descriptors to have standard output temporarily redirected to that file).
More information about capturing IO in a string and StringIO objects can be found in
Recipe 5.6. 

