==============================
14.8 创建自定义异常
==============================

----------
问题
----------
You’re building an application and would like to wrap lower-level exceptions with cus‐
tom ones that have more meaning in the context of your application.

Solution
Creating new exceptions is easy—just define them as classes that inherit from Excep
tion (or one of the other existing exception types if it makes more sense). For example,
if you are writing code related to network programming, you might define some custom
exceptions like this:

class NetworkError(Exception):
    pass

class HostnameError(NetworkError):
    pass

class TimeoutError(NetworkError):
    pass

class ProtocolError(NetworkError):
    pass

Users could then use these exceptions in the normal way. For example:

try:
    msg = s.recv()
except TimeoutError as e:
    ...
except ProtocolError as e:
    ...

Discussion
Custom exception classes should almost always inherit from the built-in Exception
class, or inherit from some locally defined base exception that itself inherits from Ex
ception. Although all exceptions also derive from BaseException, you should not use
this as a base class for new exceptions. BaseException is reserved for system-exiting
exceptions,  such  as  KeyboardInterrupt  or  SystemExit,  and  other  exceptions  that
should signal the application to exit. Therefore, catching these exceptions is not the

intended use case. Assuming you follow this convention, it follows that inheriting from
BaseException causes your custom exceptions to not be caught and to signal an im‐
minent application shutdown! 
Having custom exceptions in your application and using them as shown makes your
application code tell a more coherent story to whoever may need to read the code. One
design consideration involves the grouping of custom exceptions via inheritance. In
complicated applications, it may make sense to introduce further base classes that group
different classes of exceptions together. This gives the user a choice of catching a nar‐
rowly specified error, such as this:

try:
    s.send(msg)
except ProtocolError:
    ...

It also gives the ability to catch a broad range of errors, such as the following:

try:
    s.send(msg)
except NetworkError:
    ...

If you are going to define a new exception that overrides the __init__() method of
Exception, make sure you always call Exception.__init__() with all of the passed
arguments. For example:

class CustomError(Exception):
    def __init__(self, message, status):
        super().__init__(message, status)
        self.message = message
        self.status = status

This might look a little weird, but the default behavior of Exception is to accept all
arguments passed and to store them in the .args attribute as a tuple. Various other
libraries and parts of Python expect all exceptions to have the .args attribute, so if you
skip this step, you might find that your new exception doesn’t behave quite right in
certain contexts. To illustrate the use of .args, consider this interactive session with the
built-in RuntimeError exception, and notice how any number of arguments can be used
with the raise statement:

>>> try:
...     raise RuntimeError('It failed')
... except RuntimeError as e:
...     print(e.args)
...
('It failed',)
>>> try:
...     raise RuntimeError('It failed', 42, 'spam')
... except RuntimeError as e:

...     print(e.args)
...
('It failed', 42, 'spam')
>>>

For more information on creating your own exceptions, see the Python documentation.
