==============================
14.2 在单元测试中给对象打补丁
==============================

----------
问题
----------
You’re writing unit tests and need to apply patches to selected objects in order to make
assertions about how they were used in the test (e.g., assertions about being called with
certain parameters, access to selected attributes, etc.).

Solution
The unittest.mock.patch() function can be used to help with this problem. It’s a little
unusual, but patch() can be used as a decorator, a context manager, or stand-alone. For
example, here’s an example of how it’s used as a decorator:

from unittest.mock import patch
import example

@patch('example.func')
def test1(x, mock_func):
    example.func(x)       # Uses patched example.func
    mock_func.assert_called_with(x)
It can also be used as a context manager:

with patch('example.func') as mock_func:
    example.func(x)      # Uses patched example.func
    mock_func.assert_called_with(x)

Last, but not least, you can use it to patch things manually:

p = patch('example.func')
mock_func = p.start()
example.func(x)
mock_func.assert_called_with(x)
p.stop()

If necessary, you can stack decorators and context managers to patch multiple objects.
For example:

@patch('example.func1')
@patch('example.func2')
@patch('example.func3')
def test1(mock1, mock2, mock3):
    ...

def test2():
    with patch('example.patch1') as mock1, \
         patch('example.patch2') as mock2, \
         patch('example.patch3') as mock3:
    ...

Discussion
patch() works by taking an existing object with the fully qualified name that you pro‐
vide and replacing it with a new value. The original value is then restored after the
completion of the decorated function or context manager. By default, values are replaced
with MagicMock instances. For example:

>>> x = 42
>>> with patch('__main__.x'):
...     print(x)
...
<MagicMock name='x' id='4314230032'>
>>> x
42
>>>

However, you can actually replace the value with anything that you wish by supplying
it as a second argument to patch():

>>> x
42
>>> with patch('__main__.x', 'patched_value'):
...     print(x)
...
patched_value
>>> x
42
>>>

The MagicMock instances that are normally used as replacement values are meant to
mimic callables and instances. They record information about usage and allow you to
make assertions. For example:

>>> from unittest.mock import MagicMock
>>> m = MagicMock(return_value = 10)
>>> m(1, 2, debug=True)
10
>>> m.assert_called_with(1, 2, debug=True)
>>> m.assert_called_with(1, 2)
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File ".../unittest/mock.py", line 726, in assert_called_with
    raise AssertionError(msg)
AssertionError: Expected call: mock(1, 2)
Actual call: mock(1, 2, debug=True)
>>>

>>> m.upper.return_value = 'HELLO'
>>> m.upper('hello')
'HELLO'
>>> assert m.upper.called

>>> m.split.return_value = ['hello', 'world']
>>> m.split('hello world')
['hello', 'world']
>>> m.split.assert_called_with('hello world')
>>>

>>> m['blah']
<MagicMock name='mock.__getitem__()' id='4314412048'>
>>> m.__getitem__.called
True
>>> m.__getitem__.assert_called_with('blah')
>>>

Typically, these kinds of operations are carried out in a unit test. For example, suppose
you have some function like this:

# example.py
from urllib.request import urlopen
import csv

def dowprices():
    u = urlopen('http://finance.yahoo.com/d/quotes.csv?s=@^DJI&f=sl1')
    lines = (line.decode('utf-8') for line in u)
    rows = (row for row in csv.reader(lines) if len(row) == 2)
    prices = { name:float(price) for name, price in rows }
    return prices

Normally, this function uses urlopen() to go fetch data off the Web and parse it. To
unit test it, you might want to give it a more predictable dataset of your own creation,
however. Here’s an example using patching:

import unittest
from unittest.mock import patch
import io
import example

sample_data = io.BytesIO(b'''\
"IBM",91.1\r
"AA",13.25\r
"MSFT",27.72\r
\r
''')

class Tests(unittest.TestCase):
    @patch('example.urlopen', return_value=sample_data)
    def test_dowprices(self, mock_urlopen):
        p = example.dowprices()
        self.assertTrue(mock_urlopen.called)
        self.assertEqual(p,
                         {'IBM': 91.1,
                          'AA': 13.25,
                          'MSFT' : 27.72})

if __name__ == '__main__':
    unittest.main()

In this example, the urlopen() function in the example module is replaced with a mock
object that returns a BytesIO() containing sample data as a substitute.
An important but subtle facet of this test is the patching of example.urlopen instead of
urllib.request.urlopen. When you are making patches, you have to use the names
as they are used in the code being tested. Since the example code uses from urllib.re
quest import urlopen, the urlopen() function used by the dowprices() function is
actually located in example.
This recipe has really only given a very small taste of what’s possible with the  uni
ttest.mock module. The official documentation is a must-read for more advanced
features.
