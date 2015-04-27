==============================
9.20 利用函数注解实现方法重载
==============================

----------
问题
----------
You’ve learned about function argument annotations and you have a thought that you
might be able to use them to implement multiple-dispatch (method overloading) based
on types. However, you’re not quite sure what’s involved (or if it’s even a good idea).

|

----------
解决方案
----------
This recipe is based on a simple observation—namely, that since Python allows arguments
to be annotated, perhaps it might be possible to write code like this:

.. code-block:: python

    class Spam:
        def bar(self, x:int, y:int):
            print('Bar 1:', x, y)

        def bar(self, s:str, n:int = 0):
            print('Bar 2:', s, n)

    s = Spam()
    s.bar(2, 3) # Prints Bar 1: 2 3
    s.bar('hello') # Prints Bar 2: hello 0

Here is the start of a solution that does just that, using a combination of metaclasses and
descriptors:

.. code-block:: python

    # multiple.py
    import inspect
    import types

    class MultiMethod:
        '''
        Represents a single multimethod.
        '''
        def __init__(self, name):
            self._methods = {}
            self.__name__ = name

        def register(self, meth):
            '''
            Register a new method as a multimethod
            '''
            sig = inspect.signature(meth)

            # Build a type signature from the method's annotations
            types = []
            for name, parm in sig.parameters.items():
                if name == 'self':
                    continue
                if parm.annotation is inspect.Parameter.empty:
                    raise TypeError(
                        'Argument {} must be annotated with a type'.format(name)
                    )
                if not isinstance(parm.annotation, type):
                    raise TypeError(
                        'Argument {} annotation must be a type'.format(name)
                    )
                if parm.default is not inspect.Parameter.empty:
                    self._methods[tuple(types)] = meth
                types.append(parm.annotation)

            self._methods[tuple(types)] = meth

        def __call__(self, *args):
            '''
            Call a method based on type signature of the arguments
            '''
            types = tuple(type(arg) for arg in args[1:])
            meth = self._methods.get(types, None)
            if meth:
                return meth(*args)
            else:
                raise TypeError('No matching method for types {}'.format(types))

        def __get__(self, instance, cls):
            '''
            Descriptor method needed to make calls work in a class
            '''
            if instance is not None:
                return types.MethodType(self, instance)
            else:
                return self

    class MultiDict(dict):
        '''
        Special dictionary to build multimethods in a metaclass
        '''
        def __setitem__(self, key, value):
            if key in self:
                # If key already exists, it must be a multimethod or callable
                current_value = self[key]
                if isinstance(current_value, MultiMethod):
                    current_value.register(value)
                else:
                    mvalue = MultiMethod(key)
                    mvalue.register(current_value)
                    mvalue.register(value)
                    super().__setitem__(key, mvalue)
            else:
                super().__setitem__(key, value)

    class MultipleMeta(type):
        '''
        Metaclass that allows multiple dispatch of methods
        '''
        def __new__(cls, clsname, bases, clsdict):
            return type.__new__(cls, clsname, bases, dict(clsdict))

        @classmethod
        def __prepare__(cls, clsname, bases):
            return MultiDict()

To use this class, you write code like this:

.. code-block:: python

    class Spam(metaclass=MultipleMeta):
        def bar(self, x:int, y:int):
            print('Bar 1:', x, y)

        def bar(self, s:str, n:int = 0):
            print('Bar 2:', s, n)

    # Example: overloaded __init__
    import time

    class Date(metaclass=MultipleMeta):
        def __init__(self, year: int, month:int, day:int):
            self.year = year
            self.month = month
            self.day = day

        def __init__(self):
            t = time.localtime()
            self.__init__(t.tm_year, t.tm_mon, t.tm_mday)

Here is an interactive session that verifies that it works:

.. code-block:: python

    >>> s = Spam()
    >>> s.bar(2, 3)
    Bar 1: 2 3
    >>> s.bar('hello')
    Bar 2: hello 0
    >>> s.bar('hello', 5)
    Bar 2: hello 5
    >>> s.bar(2, 'hello')
    Traceback (most recent call last):
        File "<stdin>", line 1, in <module>
        File "multiple.py", line 42, in __call__
            raise TypeError('No matching method for types {}'.format(types))
    TypeError: No matching method for types (<class 'int'>, <class 'str'>)
    >>> # Overloaded __init__
    >>> d = Date(2012, 12, 21)
    >>> # Get today's date
    >>> e = Date()
    >>> e.year
    2012
    >>> e.month
    12
    >>> e.day
    3
    >>>

|

----------
讨论
----------
Honestly, there might be too much magic going on in this recipe to make it applicable
to real-world code. However, it does dive into some of the inner workings of metaclasses
and descriptors, and reinforces some of their concepts. Thus, even though you might
not apply this recipe directly, some of its underlying ideas might influence other programming
techniques involving metaclasses, descriptors, and function annotations.


The main idea in the implementation is relatively simple. The MutipleMeta metaclass
uses its __prepare__() method to supply a custom class dictionary as an instance of
MultiDict. Unlike a normal dictionary, MultiDict checks to see whether entries already
exist when items are set. If so, the duplicate entries get merged together inside an instance
of MultiMethod.


Instances of MultiMethod collect methods by building a mapping from type signatures
to functions. During construction, function annotations are used to collect these signatures
and build the mapping. This takes place in the MultiMethod.register()
method. One critical part of this mapping is that for multimethods, types must be
specified on all of the arguments or else an error occurs.


To make MultiMethod instances emulate a callable, the __call__() method is implemented.
This method builds a type tuple from all of the arguments except self, looks
up the method in the internal map, and invokes the appropriate method. The __get__()
is required to make MultiMethod instances operate correctly inside class definitions. In
the implementation, it’s being used to create proper bound methods. For example:

.. code-block:: python

    >>> b = s.bar
    >>> b
    <bound method Spam.bar of <__main__.Spam object at 0x1006a46d0>>
    >>> b.__self__
    <__main__.Spam object at 0x1006a46d0>
    >>> b.__func__
    <__main__.MultiMethod object at 0x1006a4d50>
    >>> b(2, 3)
    Bar 1: 2 3
    >>> b('hello')
    Bar 2: hello 0
    >>>

To be sure, there are a lot of moving parts to this recipe. However, it’s all a little unfortunate
considering how many limitations there are. For one, the solution doesn’t work
with keyword arguments: For example:

.. code-block:: python

    >>> s.bar(x=2, y=3)
    Traceback (most recent call last):
        File "<stdin>", line 1, in <module>
    TypeError: __call__() got an unexpected keyword argument 'y'

    >>> s.bar(s='hello')
    Traceback (most recent call last):
        File "<stdin>", line 1, in <module>
    TypeError: __call__() got an unexpected keyword argument 's'
    >>>

There might be some way to add such support, but it would require a completely different
approach to method mapping. The problem is that the keyword arguments don’t
arrive in any kind of particular order. When mixed up with positional arguments, you
simply get a jumbled mess of arguments that you have to somehow sort out in the
__call__() method.


This recipe is also severely limited in its support for inheritance. For example, something
like this doesn’t work:

.. code-block:: python

    class A:
        pass

    class B(A):
        pass

    class C:
        pass

    class Spam(metaclass=MultipleMeta):
        def foo(self, x:A):
            print('Foo 1:', x)

        def foo(self, x:C):
            print('Foo 2:', x)

The reason it fails is that the x:A annotation fails to match instances that are subclasses
(such as instances of B). For example:

.. code-block:: python

    >>> s = Spam()
    >>> a = A()
    >>> s.foo(a)
    Foo 1: <__main__.A object at 0x1006a5310>
    >>> c = C()
    >>> s.foo(c)
    Foo 2: <__main__.C object at 0x1007a1910>
    >>> b = B()
    >>> s.foo(b)
    Traceback (most recent call last):
        File "<stdin>", line 1, in <module>
        File "multiple.py", line 44, in __call__
            raise TypeError('No matching method for types {}'.format(types))
    TypeError: No matching method for types (<class '__main__.B'>,)
    >>>

As an alternative to using metaclasses and annotations, it is possible to implement a
similar recipe using decorators. For example:

.. code-block:: python

    import types

    class multimethod:
        def __init__(self, func):
            self._methods = {}
            self.__name__ = func.__name__
            self._default = func

        def match(self, *types):
            def register(func):
                ndefaults = len(func.__defaults__) if func.__defaults__ else 0
                for n in range(ndefaults+1):
                    self._methods[types[:len(types) - n]] = func
                return self
            return register

        def __call__(self, *args):
            types = tuple(type(arg) for arg in args[1:])
            meth = self._methods.get(types, None)
            if meth:
                return meth(*args)
            else:
                return self._default(*args)

        def __get__(self, instance, cls):
            if instance is not None:
                return types.MethodType(self, instance)
            else:
                return self

To use the decorator version, you would write code like this:

.. code-block:: python

    class Spam:
        @multimethod
        def bar(self, *args):
            # Default method called if no match
            raise TypeError('No matching method for bar')

        @bar.match(int, int)
        def bar(self, x, y):
            print('Bar 1:', x, y)

        @bar.match(str, int)
        def bar(self, s, n = 0):
            print('Bar 2:', s, n)

The decorator solution also suffers the same limitations as the previous implementation
(namely, no support for keyword arguments and broken inheritance).


All things being equal, it’s probably best to stay away from multiple dispatch in generalpurpose
code. There are special situations where it might make sense, such as in programs
that are dispatching methods based on some kind of pattern matching. For example,
perhaps the visitor pattern described in Recipe 8.21 could be recast into a class
that used multiple dispatch in some way. However, other than that, it’s usually never a
bad idea to stick with a more simple approach (simply use methods with different
names).


Ideas concerning different ways to implement multiple dispatch have floated around
the Python community for years. As a decent starting point for that discussion, see
Guido van Rossum’s blog post
`Five-Minute Multimethods in Python <http://www.artima.com/weblogs/viewpost.jsp?thread=101605>`_

