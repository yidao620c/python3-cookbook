==============================
9.17 在类上强制使用编程规约
==============================

----------
问题
----------
Your program consists of a large class hierarchy and you would like to enforce certain
kinds of coding conventions (or perform diagnostics) to help maintain programmer
sanity.

|

----------
解决方案
----------
If you want to monitor the definition of classes, you can often do it by defining a
metaclass. A basic metaclass is usually defined by inheriting from type and redefining
its __new__() method or __init__() method. For example:

.. code-block:: python

    class MyMeta(type):
        def __new__(self, clsname, bases, clsdict):
            # clsname is name of class being defined
            # bases is tuple of base classes
            # clsdict is class dictionary
            return super().__new__(cls, clsname, bases, clsdict)

Alternatively, if __init__() is defined:

.. code-block:: python

    class MyMeta(type):
        def __init__(self, clsname, bases, clsdict):
            super().__init__(clsname, bases, clsdict)
            # clsname is name of class being defined
            # bases is tuple of base classes
            # clsdict is class dictionary

To use a metaclass, you would generally incorporate it into a top-level base class from
which other objects inherit. For example:

.. code-block:: python

    class Root(metaclass=MyMeta):
        pass

    class A(Root):
        pass

    class B(Root):
        pass

A key feature of a metaclass is that it allows you to examine the contents of a class at the
time of definition. Inside the redefined __init__() method, you are free to inspect the
class dictionary, base classes, and more. Moreover, once a metaclass has been specified
for a class, it gets inherited by all of the subclasses. Thus, a sneaky framework builder
can specify a metaclass for one of the top-level classes in a large hierarchy and capture
the definition of all classes under it.

As a concrete albeit whimsical example, here is a metaclass that rejects any class definition
containing methods with mixed-case names (perhaps as a means for annoying
Java programmers):

.. code-block:: python

    class NoMixedCaseMeta(type):
        def __new__(cls, clsname, bases, clsdict):
            for name in clsdict:
                if name.lower() != name:
                    raise TypeError('Bad attribute name: ' + name)
            return super().__new__(cls, clsname, bases, clsdict)

    class Root(metaclass=NoMixedCaseMeta):
        pass

    class A(Root):
        def foo_bar(self): # Ok
            pass

    class B(Root):
        def fooBar(self): # TypeError
            pass

As a more advanced and useful example, here is a metaclass that checks the definition
of redefined methods to make sure they have the same calling signature as the original
method in the superclass.

.. code-block:: python

    from inspect import signature
    import logging

    class MatchSignaturesMeta(type):

        def __init__(self, clsname, bases, clsdict):
            super().__init__(clsname, bases, clsdict)
            sup = super(self, self)
            for name, value in clsdict.items():
                if name.startswith('_') or not callable(value):
                    continue
                # Get the previous definition (if any) and compare the signatures
                prev_dfn = getattr(sup,name,None)
                if prev_dfn:
                    prev_sig = signature(prev_dfn)
                    val_sig = signature(value)
                    if prev_sig != val_sig:
                        logging.warning('Signature mismatch in %s. %s != %s',
                                        value.__qualname__, prev_sig, val_sig)

    # Example
    class Root(metaclass=MatchSignaturesMeta):
        pass

    class A(Root):
        def foo(self, x, y):
            pass

        def spam(self, x, *, z):
            pass

    # Class with redefined methods, but slightly different signatures
    class B(A):
        def foo(self, a, b):
            pass

        def spam(self,x,z):
            pass

If you run this code, you will get output such as the following:

.. code-block:: python

    WARNING:root:Signature mismatch in B.spam. (self, x, *, z) != (self, x, z)
    WARNING:root:Signature mismatch in B.foo. (self, x, y) != (self, a, b)

Such warnings might be useful in catching subtle program bugs. For example, code that
relies on keyword argument passing to a method will break if a subclass changes the
argument names.

|

----------
讨论
----------
In large object-oriented programs, it can sometimes be useful to put class definitions
under the control of a metaclass. The metaclass can observe class definitions and be
used to alert programmers to potential problems that might go unnoticed (e.g., using
slightly incompatible method signatures).

One might argue that such errors would be better caught by program analysis tools or
IDEs. To be sure, such tools are useful. However, if you’re creating a framework or library
that’s going to be used by others, you often don’t have any control over the rigor of their
development practices. Thus, for certain kinds of applications, it might make sense to
put a bit of extra checking in a metaclass if such checking would result in a better user
experience.

The choice of redefining __new__() or __init__() in a metaclass depends on how you
want to work with the resulting class. __new__() is invoked prior to class creation and
is typically used when a metaclass wants to alter the class definition in some way (by
changing the contents of the class dictionary). The __init__() method is invoked after
a class has been created, and is useful if you want to write code that works with the fully
formed class object. In the last example, this is essential since it is using the super()
function to search for prior definitions. This only works once the class instance has been
created and the underlying method resolution order has been set.

The last example also illustrates the use of Python’s function signature objects. Essentially,
the metaclass takes each callable definition in a class, searches for a prior definition
(if any), and then simply compares their calling signatures using inspect.signature().

Last, but not least, the line of code that uses super(self, self) is not a typo. When
working with a metaclass, it’s important to realize that the self is actually a class object.
So, that statement is actually being used to find definitions located further up the class
hierarchy that make up the parents of self.


