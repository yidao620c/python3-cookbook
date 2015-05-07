==============================
14.6 处理多个异常
==============================

----------
问题
----------
You have a piece of code that can throw any of several different exceptions, and you
need to account for all of the potential exceptions that could be raised without creating
duplicate code or long, meandering code passages.

|

----------
解决方案
----------
If you can handle different exceptions all using a single block of code, they can be
grouped together in a tuple like this:

try:
    client_obj.get_url(url)
except (URLError, ValueError, SocketTimeout):
    client_obj.remove_url(url)

In the preceding example, the remove_url() method will be called if any one of the
listed exceptions occurs. If, on the other hand, you need to handle one of the exceptions
differently, put it into its own except clause:

try:
    client_obj.get_url(url)
except (URLError, ValueError):
    client_obj.remove_url(url)
except SocketTimeout:
    client_obj.handle_url_timeout(url)

Many exceptions are grouped into an inheritance hierarchy. For such exceptions, you
can catch all of them by simply specifying a base class. For example, instead of writing
code like this:

try:
    f = open(filename)
except (FileNotFoundError, PermissionError):
    ...

you could rewrite the except statement as:

try:
    f = open(filename)
except OSError:
    ...

This works because OSError is a base class that’s common to both the FileNotFound
Errorand PermissionError exceptions.

|

----------
讨论
----------
Although it’s not specific to handling multiple exceptions per se, it’s worth noting that
you can get a handle to the thrown exception using the as keyword:

try:
    f = open(filename)
except OSError as e:
    if e.errno == errno.ENOENT:
        logger.error('File not found')
    elif e.errno == errno.EACCES:
        logger.error('Permission denied')

    else:
        logger.error('Unexpected error: %d', e.errno)

In this example, the e variable holds an instance of the raised OSError. This is useful if
you need to inspect the exception further, such as processing it based on the value of an
additional status code.
Be aware that except clauses are checked in the order listed and that the first match
executes. It may be a bit pathological, but you can easily create situations where multiple
except clauses might match. For example:

>>> f = open('missing')
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
FileNotFoundError: [Errno 2] No such file or directory: 'missing'
>>> try:
...     f = open('missing')
... except OSError:
...     print('It failed')
... except FileNotFoundError:
...     print('File not found')
...
It failed
>>>

Here the  except  FileNotFoundError clause doesn’t execute because the  OSError is
more general, matches the FileNotFoundError exception, and was listed first.
As a debugging tip, if you’re not entirely sure about the class hierarchy of a particular
exception, you can quickly view it by inspecting the exception’s __mro__ attribute. For
example:

>>> FileNotFoundError.__mro__
(<class 'FileNotFoundError'>, <class 'OSError'>, <class 'Exception'>,
 <class 'BaseException'>, <class 'object'>)
>>>

Any one of the listed classes up to BaseException can be used with the except statement.

