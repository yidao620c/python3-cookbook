============================
10.4 将模块分割成多个文件
============================

----------
问题
----------
You have a module that you would like to split into multiple files. However, you would
like to do it without breaking existing code by keeping the separate files unified as a
single logical module.

|

----------
解决方案
----------
A program module can be split into separate files by turning it into a package. Consider
the following simple module:

.. code-block:: python

    # mymodule.py
    class A:
        def spam(self):
            print('A.spam')

    class B(A):
        def bar(self):
            print('B.bar')

Suppose you want to split mymodule.py into two files, one for each class definition. To
do that, start by replacing the mymodule.py file with a directory called mymodule. In
that directory, create the following files:

.. code-block:: python

    mymodule/
        __init__.py
        a.py
        b.py

In the a.py file, put this code:

.. code-block:: python

    # a.py
    class A:
        def spam(self):
            print('A.spam')

In the b.py file, put this code:

.. code-block:: python

    # b.py
    from .a import A
    class B(A):
        def bar(self):
            print('B.bar')

Finally, in the __init__.py file, glue the two files together:

.. code-block:: python

    # __init__.py
    from .a import A
    from .b import B

If you follow these steps, the resulting mymodule package will appear to be a single logical
module:

.. code-block:: python

    >>> import mymodule
    >>> a = mymodule.A()
    >>> a.spam()
    A.spam
    >>> b = mymodule.B()
    >>> b.bar()
    B.bar
    >>>

|

----------
讨论
----------
The primary concern in this recipe is a design question of whether or not you want
users to work with a lot of small modules or just a single module. For example, in a large
code base, you could just break everything up into separate files and make users use a
lot of import statements like this:

.. code-block:: python

    from mymodule.a import A
    from mymodule.b import B
    ...

This works, but it places more of a burden on the user to know where the different parts
are located. Often, it’s just easier to unify things and allow a single import like this:

.. code-block:: python

    from mymodule import A, B

For this latter case, it’s most common to think of mymodule as being one large source
file. However, this recipe shows how to stitch multiple files together into a single logical
namespace. The key to doing this is to create a package directory and to use the
__init__.py file to glue the parts together.


When a module gets split, you’ll need to pay careful attention to cross-filename references.
For instance, in this recipe, class B needs to access class A as a base class. A packagerelative
import from .a import A is used to get it.


Package-relative imports are used throughout the recipe to avoid hardcoding the toplevel
module name into the source code. This makes it easier to rename the module or
move it around elsewhere later (see Recipe 10.3).


One extension of this recipe involves the introduction of “lazy” imports. As shown, the
__init__.py file imports all of the required subcomponents all at once. However, for a
very large module, perhaps you only want to load components as they are needed. To
do that, here is a slight variation of __init__.py:

.. code-block:: python

    # __init__.py
    def A():
        from .a import A
        return A()

    def B():
        from .b import B
        return B()

In this version, classes A and B have been replaced by functions that load the desired
classes when they are first accessed. To a user, it won’t look much different. For example:

.. code-block:: python

    >>> import mymodule
    >>> a = mymodule.A()
    >>> a.spam()
    A.spam
    >>>

The main downside of lazy loading is that inheritance and type checking might break.
For example, you might have to change your code slightly:

.. code-block:: python

    if isinstance(x, mymodule.A): # Error
    ...

    if isinstance(x, mymodule.a.A): # Ok
    ...

For a real-world example of lazy loading, look at the source code for multiprocessing/
__init__.py in the standard library.


