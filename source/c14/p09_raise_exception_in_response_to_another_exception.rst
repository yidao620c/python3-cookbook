==============================
14.9 捕获异常后抛出另外的异常
==============================

----------
问题
----------
You want to raise an exception in response to catching a different exception, but want
to include information about both exceptions in the traceback.

Solution
To chain exceptions, use the raise from statement instead of a simple raise statement.
This will give you information about both errors. For example:

>>> def example():
...     try:
...             int('N/A')
...     except ValueError as e:
...             raise RuntimeError('A parsing error occurred') from e...
>>> 
example()
Traceback (most recent call last):
  File "<stdin>", line 3, in example
ValueError: invalid literal for int() with base 10: 'N/A'

The above exception was the direct cause of the following exception:

Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "<stdin>", line 5, in example
RuntimeError: A parsing error occurred
>>>

As you can see in the traceback, both exceptions are captured. To catch such an excep‐
tion, you would use a normal except statement. However, you can look at the __cause__
attribute of the exception object to follow the exception chain should you wish. For
example:
try:
    example()
except RuntimeError as e:
    print("It didn't work:", e)

    if e.__cause__:
        print('Cause:', e.__cause__)

An implicit form of chained exceptions occurs when another exception gets raised in‐
side an except block. For example:

>>> def example2():
...     try:
...             int('N/A')
...     except ValueError as e:
...             print("Couldn't parse:", err)
...
>>>
>>> example2()
Traceback (most recent call last):
  File "<stdin>", line 3, in example2
ValueError: invalid literal for int() with base 10: 'N/A'

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "<stdin>", line 5, in example2
NameError: global name 'err' is not defined
>>>

In this example, you get information about both exceptions, but the interpretation is a
bit different. In this case, the NameError exception is raised as the result of a program‐
ming error, not in direct response to the parsing error. For this case, the __cause__
attribute of an exception is not set. Instead, a __context__ attribute is set to the prior
exception.
If, for some reason, you want to suppress chaining, use raise from None:

>>> def example3():
...     try:
...             int('N/A')
...     except ValueError:
...             raise RuntimeError('A parsing error occurred') from None...
>>> 
example3()
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "<stdin>", line 5, in example3
RuntimeError: A parsing error occurred
>>>

Discussion
In designing code, you should give careful attention to use of the raise statement inside
of  other  except  blocks.  In  most  cases,  such  raise  statements  should  probably  be
changed to raise from statements. That is, you should prefer this style:

try:
   ...
except SomeException as e:
   raise DifferentException() from e

The reason for doing this is that you are explicitly chaining the causes together. That is,
the  DifferentException  is  being  raised  in  direct  response  to  getting  a  SomeExcep
tion. This relationship will be explicitly stated in the resulting traceback.
If you write your code in the following style, you still get a chained exception, but it’s
often not clear if the exception chain was intentional or the result of an unforeseen
programming error:

try:
   ...
except SomeException:
   raise DifferentException()

When you use raise from, you’re making it clear that you meant to raise the second
exception.
Resist the urge to suppress exception information, as shown in the last example. Al‐
though suppressing exception information can lead to smaller tracebacks, it also dis‐
cards information that might be useful for debugging. All things being equal, it’s often
best to keep as much information as possible.
