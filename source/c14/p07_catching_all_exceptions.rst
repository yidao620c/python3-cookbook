==============================
14.7 捕获所有异常
==============================

----------
问题
----------
You want to write code that catches all exceptions.

Solution
To catch all exceptions, write an exception handler for Exception, as shown here:

try:
   ...
except Exception as e:
   ...
   log('Reason:', e)       # Important!

This will catch all exceptions save SystemExit, KeyboardInterrupt, and GeneratorEx
it. If you also want to catch those exceptions, change Exception to BaseException.

Discussion
Catching all exceptions is sometimes used as a crutch by programmers who can’t re‐
member all of the possible exceptions that might occur in complicated operations. As
such, it is also a very good way to write undebuggable code if you are not careful.
Because of this, if you choose to catch all exceptions, it is absolutely critical to log or
report the actual reason for the exception somewhere (e.g., log file, error message print‐
ed to screen, etc.). If you don’t do this, your head will likely explode at some point.
Consider this example:

def parse_int(s):
    try:
        n = int(v)
    except Exception:
        print("Couldn't parse")

If you try this function, it behaves like this:

>>> parse_int('n/a')
Couldn't parse
>>> parse_int('42')
Couldn't parse
>>>

At this point, you might be left scratching your head as to why it doesn’t work. Now
suppose the function had been written like this:

def parse_int(s):
    try:
        n = int(v)
    except Exception as e:
        print("Couldn't parse")
        print('Reason:', e)

In this case, you get the following output, which indicates that a programming mistake
has been made:

>>> parse_int('42')
Couldn't parse
Reason: global name 'v' is not defined
>>>

All things being equal, it’s probably better to be as precise as possible in your exception
handling. However, if you must catch all exceptions, just make sure you give good di‐
agnostic information or propagate the exception so that cause doesn’t get lost.
