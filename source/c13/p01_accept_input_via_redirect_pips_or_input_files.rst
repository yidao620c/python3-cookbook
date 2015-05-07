==============================
13.1 通过重定向/管道/文件接受输入
==============================

----------
问题
----------
You want a script you’ve written to be able to accept input using whatever mechanism
is easiest for the user. This should include piping output from a command to the script,
redirecting a file into the script, or just passing a filename, or list of filenames, to the
script on the command line.

Solution
Python’s built-in fileinput module makes this very simple and concise. If you have a
script that looks like this:
#!/usr/bin/env python3
import fileinput

with fileinput.input() as f_input:
    for line in f_input:
        print(line, end='')

Then you can already accept input to the script in all of the previously mentioned ways.
If you save this script as filein.py and make it executable, you can do all of the following
and get the expected output:

$ ls | ./filein.py          # Prints a directory listing to stdout.
$ ./filein.py /etc/passwd   # Reads /etc/passwd to stdout.
$ ./filein.py < /etc/passwd # Reads /etc/passwd to stdout.

Discussion
The  fileinput.input() function creates and returns an instance of the  FileInput
class. In addition to containing a few handy helper methods, the instance can also be
used as a context manager. So, to put all of this together, if we wrote a script that expected
to be printing output from several files at once, we might have it include the filename
and line number in the output, like this:

>>> import fileinput
>>> with fileinput.input('/etc/passwd') as f:
>>>     for line in f:
...         print(f.filename(), f.lineno(), line, end='')
...
/etc/passwd 1 ##
/etc/passwd 2 # User Database
/etc/passwd 3 #

<other output omitted>

Using it as a context manager ensures that the file is closed when it’s no longer being
used, and we leveraged a few handy FileInput helper methods here to get some extra
information in the output.
