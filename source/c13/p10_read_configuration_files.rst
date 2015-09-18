==============================
13.10 读取配置文件
==============================

----------
问题
----------
You  want  to  read  configuration  files  written  in  the  common  .ini  configuration  file
format.

|

----------
解决方案
----------
The configparser module can be used to read configuration files. For example, suppose
you have this configuration file:

; config.ini
; Sample configuration file

[installation]
library=%(prefix)s/lib
include=%(prefix)s/include
bin=%(prefix)s/bin
prefix=/usr/local

# Setting related to debug configuration
[debug]
log_errors=true
show_warnings=False

[server]
port: 8080
nworkers: 32
pid-file=/tmp/spam.pid
root=/www/root
signature:
    =================================
    Brought to you by the Python Cookbook
    =================================

Here is an example of how to read it and extract values:

>>> from configparser import ConfigParser
>>> cfg = ConfigParser()
>>> cfg.read('config.ini')
['config.ini']
>>> cfg.sections()
['installation', 'debug', 'server']
>>> cfg.get('installation','library')
'/usr/local/lib'
>>> cfg.getboolean('debug','log_errors')

True
>>> cfg.getint('server','port')
8080
>>> cfg.getint('server','nworkers')
32
>>> print(cfg.get('server','signature'))

\=================================
Brought to you by the Python Cookbook
\=================================
>>>

If desired, you can also modify the configuration and write it back to a file using the
cfg.write() method. For example:

>>> cfg.set('server','port','9000')
>>> cfg.set('debug','log_errors','False')
>>> import sys
>>> cfg.write(sys.stdout)
[installation]
library = %(prefix)s/lib
include = %(prefix)s/include
bin = %(prefix)s/bin
prefix = /usr/local

[debug]
log_errors = False
show_warnings = False

[server]
port = 9000
nworkers = 32
pid-file = /tmp/spam.pid
root = /www/root
signature =
          =================================
          Brought to you by the Python Cookbook
          =================================
>>>

|

----------
讨论
----------
Configuration files are well suited as a human-readable format for specifying configu‐
ration data to your program. Within each config file, values are grouped into different
sections (e.g., “installation,” “debug,” and “server,” in the example). Each section then
specifies values for various variables in that section.
There are several notable differences between a config file and using a Python source
file for the same purpose. First, the syntax is much more permissive and “sloppy.” For
example, both of these assignments are equivalent:

prefix=/usr/local
prefix: /usr/local

The names used in a config file are also assumed to be case-insensitive. For example:

>>> cfg.get('installation','PREFIX')
'/usr/local'
>>> cfg.get('installation','prefix')
'/usr/local'
>>>

When parsing values, methods such as getboolean() look for any reasonable value.
For example, these are all equivalent:

    log_errors = true
    log_errors = TRUE
    log_errors = Yes
    log_errors = 1

Perhaps the most significant difference between a config file and Python code is that,
unlike scripts, configuration files are not executed in a top-down manner. Instead, the
file is read in its entirety. If variable substitutions are made, they are done after the fact.
For example, in this part of the config file, it doesn’t matter that the prefix variable is
assigned after other variables that happen to use it:

    [installation]
    library=%(prefix)s/lib
    include=%(prefix)s/include
    bin=%(prefix)s/bin
    prefix=/usr/local

An easily overlooked feature of ConfigParser is that it can read multiple configuration
files together and merge their results into a single configuration. For example, suppose
a user made their own configuration file that looked like this:

    ; ~/.config.ini
    [installation]
    prefix=/Users/beazley/test

    [debug]
    log_errors=False

This file can be merged with the previous configuration by reading it separately. For
example:

>>> # Previously read configuration
>>> cfg.get('installation', 'prefix')
'/usr/local'

>>> # Merge in user-specific configuration
>>> import os
>>> cfg.read(os.path.expanduser('~/.config.ini'))
['/Users/beazley/.config.ini']

>>> cfg.get('installation', 'prefix')
'/Users/beazley/test'
>>> cfg.get('installation', 'library')
'/Users/beazley/test/lib'
>>> cfg.getboolean('debug', 'log_errors')
False
>>>

Observe how the override of the prefix variable affects other related variables, such as
the setting of library. This works because variable interpolation is performed as late
as possible. You can see this by trying the following experiment:

>>> cfg.get('installation','library')
'/Users/beazley/test/lib'
>>> cfg.set('installation','prefix','/tmp/dir')
>>> cfg.get('installation','library')
'/tmp/dir/lib'
>>>

Finally, it’s important to note that Python does not support the full range of features you
might find in an .ini file used by other programs (e.g., applications on Windows). Make
sure you consult the configparser documentation for the finer details of the syntax
and supported features. 
