==============================
13.12 给内库增加日志功能
==============================

----------
问题
----------
You would like to add a logging capability to a library, but don’t want it to interfere with
programs that don’t use logging.

Solution
For libraries that want to perform logging, you should create a dedicated logger object,
and initially configure it as follows:

# somelib.py

import logging
log = logging.getLogger(__name__)
log.addHandler(logging.NullHandler())

# Example function (for testing)
def func():
    log.critical('A Critical Error!')
    log.debug('A debug message')

With this configuration, no logging will occur by default. For example:

>>> import somelib
>>> somelib.func()
>>>

However, if the logging system gets configured, log messages will start to appear. For
example:

>>> import logging
>>> logging.basicConfig()
>>> somelib.func()
CRITICAL:somelib:A Critical Error!
>>>

Discussion
Libraries present a special problem for logging, since information about the environ‐
ment in which they are used isn’t known. As a general rule, you should never write
library code that tries to configure the logging system on its own or which makes as‐
sumptions about an already existing logging configuration. Thus, you need to take great
care to provide isolation.
The call to getLogger(__name__) creates a logger module that has the same name as
the calling module. Since all modules are unique, this creates a dedicated logger that is
likely to be separate from other loggers.

The log.addHandler(logging.NullHandler()) operation attaches a null handler to
the just created logger object. A null handler ignores all logging messages by default.
Thus, if the library is used and logging is never configured, no messages or warnings
will appear.
One subtle feature of this recipe is that the logging of individual libraries can be inde‐
pendently configured, regardless of other logging settings. For example, consider the
following code:

>>> import logging
>>> logging.basicConfig(level=logging.ERROR)
>>> import somelib
>>> somelib.func()
CRITICAL:somelib:A Critical Error!

>>> # Change the logging level for 'somelib' only
>>> logging.getLogger('somelib').level=logging.DEBUG
>>> somelib.func()
CRITICAL:somelib:A Critical Error!
DEBUG:somelib:A debug message
>>>

Here, the root logger has been configured to only output messages at the ERROR level or
higher. However, the level of the logger for somelib has been separately configured to
output debugging messages. That setting takes precedence over the global setting.
The ability to change the logging settings for a single module like this can be a useful
debugging tool, since you don’t have to change any of the global logging settings—simply
change the level for the one module where you want more output.
The “Logging HOWTO” has more information about configuring the logging module
and other useful tips.
