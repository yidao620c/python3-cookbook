==============================
14.10 重新抛出最后的异常
==============================

----------
问题
----------
You caught an exception in an except block, but now you want to reraise it.

|

----------
解决方案
----------
Simply use the raise statement all by itself. For example:

>>> def example():
...     try:
...             int('N/A')
...     except ValueError:
...             print("Didn't work")
...             raise
...

>>> example()
Didn't work
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "<stdin>", line 3, in example
ValueError: invalid literal for int() with base 10: 'N/A'
>>>

|

----------
讨论
----------
This problem typically arises when you need to take some kind of action in response to
an exception (e.g., logging, cleanup, etc.), but afterward, you simply want to propagate
the exception along. A very common use might be in catch-all exception handlers:

try:
   ...
except Exception as e:
   # Process exception information in some way
   ...

   # Propagate the exception
   raise

