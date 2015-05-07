==============================
14.14 让你的程序跑的更快
==============================

----------
问题
----------
Your program runs too slow and you’d like to speed it up without the assistance of more
extreme solutions, such as C extensions or a just-in-time (JIT) compiler.

Solution
While the first rule of optimization might be to “not do it,” the second rule is almost
certainly “don’t optimize the unimportant.” To that end, if your program is running slow,
you might start by profiling your code as discussed in Recipe 14.13.
More often than not, you’ll find that your program spends its time in a few hotspots,
such as inner data processing loops. Once you’ve identified those locations, you can use
the no-nonsense techniques presented in the following sections to make your program
run faster.

Use functions
A lot of programmers start using Python as a language for writing simple scripts. When
writing scripts, it is easy to fall into a practice of simply writing code with very little
structure. For example:

# somescript.py

import sys
import csv

with open(sys.argv[1]) as f:
     for row in csv.reader(f):

         # Some kind of processing
         ...

A little-known fact is that code defined in the global scope like this runs slower than
code defined in a function. The speed difference has to do with the implementation of
local versus global variables (operations involving locals are faster). So, if you want to
make the program run faster, simply put the scripting statements in a function:

# somescript.py
import sys
import csv

def main(filename):
    with open(filename) as f:
         for row in csv.reader(f):
             # Some kind of processing
             ...

main(sys.argv[1])

The speed difference depends heavily on the processing being performed, but in our
experience, speedups of 15-30% are not uncommon.

Selectively eliminate attribute access
Every use of the dot (.) operator to access attributes comes with a cost. Under the covers,
this triggers special methods, such as __getattribute__() and __getattr__(), which
often lead to dictionary lookups.
You can often avoid attribute lookups by using the from module import name form of
import as well as making selected use of bound methods. To illustrate, consider the
following code fragment:

import math

def compute_roots(nums):
    result = []
    for n in nums:
        result.append(math.sqrt(n))
    return result

# Test
nums = range(1000000)
for n in range(100):
    r = compute_roots(nums)

When tested on our machine, this program runs in about 40 seconds. Now change the
compute_roots() function as follows:

from math import sqrt

def compute_roots(nums):

    result = []
    result_append = result.append
    for n in nums:
        result_append(sqrt(n))
    return result

This version runs in about 29 seconds. The only difference between the two versions of
code is the elimination of attribute access. Instead of using math.sqrt(), the code uses
sqrt(). The result.append() method is additionally placed into a local variable re
sult_append and reused in the inner loop.
However, it must be emphasized that these changes only make sense in frequently ex‐
ecuted code, such as loops. So, this optimization really only makes sense in carefully 
selected places.

Understand locality of variables
As previously noted, local variables are faster than global variables. For frequently ac‐
cessed names, speedups can be obtained by making those names as local as possible.
For  example,  consider  this  modified  version  of  the  compute_roots()  function  just
discussed:

import math

def compute_roots(nums):
    sqrt = math.sqrt
    result = []
    result_append = result.append
    for n in nums:
        result_append(sqrt(n))
    return result

In this version,  sqrt has been lifted from the  math module and placed into a local
variable. If you run this code, it now runs in about 25 seconds (an improvement over
the previous version, which took 29 seconds). That additional speedup is due to a local
lookup of sqrt being a bit faster than a global lookup of sqrt.
Locality arguments also apply when working in classes. In general, looking up a value
such as self.name will be considerably slower than accessing a local variable. In inner
loops, it might pay to lift commonly accessed attributes into a local variable. For example:

# Slower
class SomeClass:
    ...
    def method(self):
         for x in s:
             op(self.value)

# Faster
class SomeClass:

    ...
    def method(self):
         value = self.value
         for x in s:
             op(value)

Avoid gratuitous abstraction
Any time you wrap up code with extra layers of processing, such as decorators, prop‐
erties, or descriptors, you’re going to make it slower. As an example, consider this class:

class A:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    @property
    def y(self):
        return self._y
    @y.setter
    def y(self, value):
        self._y = value

Now, try a simple timing test:

>>> from timeit import timeit
>>> a = A(1,2)
>>> timeit('a.x', 'from __main__ import a')
0.07817923510447145
>>> timeit('a.y', 'from __main__ import a')
0.35766440676525235
>>>

As you can observe, accessing the property y is not just slightly slower than a simple
attribute x, it’s about 4.5 times slower. If this difference matters, you should ask yourself
if the definition of y as a property was really necessary. If not, simply get rid of it and
go back to using a simple attribute instead. Just because it might be common for pro‐
grams in another programming language to use getter/setter functions, that doesn’t
mean you should adopt that programming style for Python.

Use the built-in containers
Built-in data types such as strings, tuples, lists, sets, and dicts are all implemented in C,
and are rather fast. If you’re inclined to make your own data structures as a replacement
(e.g., linked lists, balanced trees, etc.), it may be rather difficult if not impossible to match
the speed of the built-ins. Thus, you’re often better off just using them.

Avoid making unnecessary data structures or copies
Sometimes programmers get carried away with making unnecessary data structures
when they just don’t have to. For example, someone might write code like this:

values = [x for x in sequence]
squares = [x*x for x in values]

Perhaps the thinking here is to first collect a bunch of values into a list and then to start
applying operations such as list comprehensions to it. However, the first list is com‐
pletely unnecessary. Simply write the code like this:

squares = [x*x for x in sequence]

Related to this, be on the lookout for code written by programmers who are overly
paranoid about Python’s sharing of values. Overuse of functions such as copy.deep
copy() may be a sign of code that’s been written by someone who doesn’t fully under‐
stand or trust Python’s memory model. In such code, it may be safe to eliminate many
of the copies.

Discussion
Before optimizing, it’s usually worthwhile to study the algorithms that you’re using first.
You’ll get a much bigger speedup by switching to an O(n log n) algorithm than by
trying to tweak the implementation of an an O(n**2) algorithm.
If you’ve decided that you still must optimize, it pays to consider the big picture. As a
general rule, you don’t want to apply optimizations to every part of your program,
because such changes are going to make the code hard to read and understand. Instead,
focus only on known performance bottlenecks, such as inner loops.
You need to be especially wary interpreting the results of micro-optimizations. For
example, consider these two techniques for creating a dictionary:

a = {
    'name' : 'AAPL',
    'shares' : 100,
    'price' : 534.22
}

b = dict(name='AAPL', shares=100, price=534.22)

The latter choice has the benefit of less typing (you don’t need to quote the key names).
However, if you put the two code fragments in a head-to-head performance battle, you’ll
find that using  dict() runs three times slower! With this knowledge, you might be
inclined to scan your code and replace every use of dict() with its more verbose al‐
ternative. However, a smart programmer will only focus on parts of a program where
it might actually matter, such as an inner loop. In other places, the speed difference just
isn’t going to matter at all.
If, on the other hand, your performance needs go far beyond the simple techniques in
this recipe, you might investigate the use of tools based on just-in-time (JIT) compilation
techniques. For example, the PyPy project is an alternate implementation of the Python

interpreter that analyzes the execution of your program and generates native machine
code for frequently executed parts. It can sometimes make Python programs run an
order of magnitude faster, often approaching (or even exceeding) the speed of code
written in C. Unfortunately, as of this writing, PyPy does not yet fully support Python
3. So, that is something to look for in the future. You might also consider the Numba
project. Numba is a dynamic compiler where you annotate selected Python functions
that you want to optimize with a decorator. Those functions are then compiled into
native machine code through the use of LLVM. It too can produce signficant perfor‐
mance gains. However, like PyPy, support for Python 3 should be viewed as somewhat
experimental.
Last, but not least, the words of John Ousterhout come to mind: “The best performance
improvement is the transition from the nonworking to the working state.” Don’t worry
about optimization until you need to. Making sure your program works correctly is
usually more important than making it run fast (at least initially).


