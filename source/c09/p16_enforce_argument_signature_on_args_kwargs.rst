===============================
9.16 强制*args和**kwargs的参数签名
===============================

----------
问题
----------
You’ve written a function or method that uses *args and **kwargs, so that it can be
general purpose, but you would also like to check the passed arguments to see if they
match a specific function calling signature.

|

----------
解决方案
----------
For any problem where you want to manipulate function calling signatures, you should
use the signature features found in the inspect module. Two classes, Signature and
Parameter, are of particular interest here. Here is an interactive example of creating a
function signature:

.. code-block:: python

    >>> from inspect import Signature, Parameter
    >>> # Make a signature for a func(x, y=42, *, z=None)
    >>> parms = [ Parameter('x', Parameter.POSITIONAL_OR_KEYWORD),
    ...         Parameter('y', Parameter.POSITIONAL_OR_KEYWORD, default=42),
    ...         Parameter('z', Parameter.KEYWORD_ONLY, default=None) ]
    >>> sig = Signature(parms)
    >>> print(sig)
    (x, y=42, *, z=None)
    >>>

Once you have a signature object, you can easily bind it to *args and **kwargs using
the signature’s bind() method, as shown in this simple example:

.. code-block:: python

    >>> def func(*args, **kwargs):
    ...     bound_values = sig.bind(*args, **kwargs)
    ...     for name, value in bound_values.arguments.items():
    ...         print(name,value)
    ...
    >>> # Try various examples
    >>> func(1, 2, z=3)
    x 1
    y 2
    z 3
    >>> func(1)
    x 1
    >>> func(1, z=3)
    x 1
    z 3
    >>> func(y=2, x=1)
    x 1
    y 2
    >>> func(1, 2, 3, 4)
    Traceback (most recent call last):
    ...
        File "/usr/local/lib/python3.3/inspect.py", line 1972, in _bind
            raise TypeError('too many positional arguments')
    TypeError: too many positional arguments
    >>> func(y=2)
    Traceback (most recent call last):
    ...
        File "/usr/local/lib/python3.3/inspect.py", line 1961, in _bind
            raise TypeError(msg) from None
    TypeError: 'x' parameter lacking default value
    >>> func(1, y=2, x=3)
    Traceback (most recent call last):
    ...
        File "/usr/local/lib/python3.3/inspect.py", line 1985, in _bind
            '{arg!r}'.format(arg=param.name))
    TypeError: multiple values for argument 'x'
    >>>

As you can see, the binding of a signature to the passed arguments enforces all of the
usual function calling rules concerning required arguments, defaults, duplicates, and
so forth.

Here is a more concrete example of enforcing function signatures. In this code, a base
class has defined an extremely general-purpose version of __init__(), but subclasses
are expected to supply an expected signature.

.. code-block:: python

    from inspect import Signature, Parameter

    def make_sig(*names):
        parms = [Parameter(name, Parameter.POSITIONAL_OR_KEYWORD)
                for name in names]
        return Signature(parms)

    class Structure:
        __signature__ = make_sig()
        def __init__(self, *args, **kwargs):
            bound_values = self.__signature__.bind(*args, **kwargs)
            for name, value in bound_values.arguments.items():
                setattr(self, name, value)

    # Example use
    class Stock(Structure):
        __signature__ = make_sig('name', 'shares', 'price')

    class Point(Structure):
        __signature__ = make_sig('x', 'y')

Here is an example of how the Stock class works:

.. code-block:: python

    >>> import inspect
    >>> print(inspect.signature(Stock))
    (name, shares, price)
    >>> s1 = Stock('ACME', 100, 490.1)
    >>> s2 = Stock('ACME', 100)
    Traceback (most recent call last):
    ...
    TypeError: 'price' parameter lacking default value
    >>> s3 = Stock('ACME', 100, 490.1, shares=50)
    Traceback (most recent call last):
    ...
    TypeError: multiple values for argument 'shares'
    >>>


----------
讨论
----------
The use of functions involving *args and **kwargs is very common when trying to
make general-purpose libraries, write decorators or implement proxies. However, one
downside of such functions is that if you want to implement your own argument checking,
it can quickly become an unwieldy mess. As an example, see Recipe 8.11. The use
of a signature object simplifies this.

In the last example of the solution, it might make sense to create signature objects
through the use of a custom metaclass. Here is an alternative implementation that shows
how to do this:

.. code-block:: python

    from inspect import Signature, Parameter

    def make_sig(*names):
        parms = [Parameter(name, Parameter.POSITIONAL_OR_KEYWORD)
                for name in names]
        return Signature(parms)

    class StructureMeta(type):
        def __new__(cls, clsname, bases, clsdict):
            clsdict['__signature__'] = make_sig(*clsdict.get('_fields',[]))
            return super().__new__(cls, clsname, bases, clsdict)

    class Structure(metaclass=StructureMeta):
        _fields = []
        def __init__(self, *args, **kwargs):
            bound_values = self.__signature__.bind(*args, **kwargs)
            for name, value in bound_values.arguments.items():
                setattr(self, name, value)

    # Example
    class Stock(Structure):
        _fields = ['name', 'shares', 'price']

    class Point(Structure):
        _fields = ['x', 'y']

When defining custom signatures, it is often useful to store the signature in a special
attribute __signature__, as shown. If you do this, code that uses the inspect module
to perform introspection will see the signature and report it as the calling convention.
For example:

.. code-block:: python

    >>> import inspect
    >>> print(inspect.signature(Stock))
    (name, shares, price)
    >>> print(inspect.signature(Point))
    (x, y)
    >>>

