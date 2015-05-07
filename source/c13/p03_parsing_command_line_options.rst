==============================
13.3 解析命令行选项
==============================

----------
问题
----------
You want to write a program that parses options supplied on the command line (found
in sys.argv).

|

----------
解决方案
----------
The argparse module can be used to parse command-line options. A simple example
will help to illustrate the essential features:

# search.py
'''
Hypothetical command-line tool for searching a collection of
files for one or more text patterns.
'''
import argparse
parser = argparse.ArgumentParser(description='Search some files')

parser.add_argument(dest='filenames',metavar='filename', nargs='*')

parser.add_argument('-p', '--pat',metavar='pattern', required=True,
                    dest='patterns', action='append',
                    help='text pattern to search for')

parser.add_argument('-v', dest='verbose', action='store_true',
                    help='verbose mode')

parser.add_argument('-o', dest='outfile', action='store',
                    help='output file')

parser.add_argument('--speed', dest='speed', action='store',
                    choices={'slow','fast'}, default='slow',
                    help='search speed')

args = parser.parse_args()

# Output the collected arguments
print(args.filenames)
print(args.patterns)
print(args.verbose)
print(args.outfile)
print(args.speed)

This program defines a command-line parser with the following usage:

bash % python3 search.py -h
usage: search.py [-h] [-p pattern] [-v] [-o OUTFILE] [--speed {slow,fast}]
                 [filename [filename ...]]

Search some files

positional arguments:
  filename

optional arguments:
  -h, --help            show this help message and exit
  -p pattern, --pat pattern
                        text pattern to search for
  -v                    verbose mode
  -o OUTFILE            output file
  --speed {slow,fast}   search speed

The following session shows how data shows up in the program. Carefully observe the
output of the print() statements.

bash % python3 search.py foo.txt bar.txt
usage: search.py [-h] -p pattern [-v] [-o OUTFILE] [--speed {fast,slow}]
                 [filename [filename ...]]
search.py: error: the following arguments are required: -p/--pat

bash % python3 search.py -v -p spam --pat=eggs foo.txt bar.txt
filenames = ['foo.txt', 'bar.txt']
patterns  = ['spam', 'eggs']
verbose   = True
outfile   = None
speed     = slow

bash % python3 search.py -v -p spam --pat=eggs foo.txt bar.txt -o results
filenames = ['foo.txt', 'bar.txt']
patterns  = ['spam', 'eggs']
verbose   = True
outfile   = results
speed     = slow

bash % python3 search.py -v -p spam --pat=eggs foo.txt bar.txt -o results \
             --speed=fast
filenames = ['foo.txt', 'bar.txt']
patterns  = ['spam', 'eggs']
verbose   = True
outfile   = results
speed     = fast

Further processing of the options is up to the program. Replace the print() functions
with something more interesting.

|

----------
讨论
----------
The argparse module is one of the largest modules in the standard library, and has a
huge number of configuration options. This recipe shows an essential subset that can
be used and extended to get started.
To parse options, you first create an ArgumentParser instance and add declarations for
the options you want to support it using the add_argument() method. In each add_ar
gument() call, the dest argument specifies the name of an attribute where the result of
parsing will be placed. The metavar argument is used when generating help messages.
The action argument specifies the processing associated with the argument and is often
store for storing a value or append for collecting multiple argument values into a list.
The following argument collects all of the extra command-line arguments into a list. It’s
being used to make a list of filenames in the example:

parser.add_argument(dest='filenames',metavar='filename', nargs='*')

The following argument sets a Boolean flag depending on whether or not the argument
was provided:

parser.add_argument('-v', dest='verbose', action='store_true',
                    help='verbose mode')

The following argument takes a single value and stores it as a string:

parser.add_argument('-o', dest='outfile', action='store',
                    help='output file')

The following argument specification allows an argument to be repeated multiple times
and all of the values append into a list. The required flag means that the argument must
be supplied at least once. The use of -p and --pat mean that either argument name is
acceptable.

parser.add_argument('-p', '--pat',metavar='pattern', required=True,
                    dest='patterns', action='append',
                    help='text pattern to search for')

Finally, the following argument specification takes a value, but checks it against a set of
possible choices.

parser.add_argument('--speed', dest='speed', action='store',
                    choices={'slow','fast'}, default='slow',
                    help='search speed')

Once the options have been given, you simply execute the parser.parse() method.
This will process the sys.argv value and return an instance with the results. The results

for each argument are placed into an attribute with the name given in the dest parameter
to add_argument().
There are several other approaches for parsing command-line options. For example,
you might be inclined to manually process sys.argv yourself or use the getopt module
(which is modeled after a similarly named C library). However, if you take this approach,
you’ll simply end up replicating much of the code that argparse already provides. You
may also encounter code that uses the  optparse library to parse options. Although
optparse is very similar to argparse, the latter is more modern and should be preferred
in new projects.
