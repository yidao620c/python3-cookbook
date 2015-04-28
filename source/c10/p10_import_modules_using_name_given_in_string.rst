================================
10.10 通过字符串名导入模块
================================

----------
问题
----------
You have the name of a module that you would like to import, but it’s being held in a
string. You would like to invoke the import command on the string.

|

----------
解决方案
----------
Use the importlib.import_module() function to manually import a module or part of
a package where the name is given as a string. For example:

.. code-block:: python

    >>> import importlib
    >>> math = importlib.import_module('math')
    >>> math.sin(2)
    0.9092974268256817
    >>> mod = importlib.import_module('urllib.request')
    >>> u = mod.urlopen('http://www.python.org')
    >>>

import_module simply performs the same steps as import, but returns the resulting
module object back to you as a result. You just need to store it in a variable and use it
like a normal module afterward.


If you are working with packages, import_module() can also be used to perform relative
imports. However, you need to give it an extra argument. For example:

.. code-block:: python

    import importlib
    # Same as 'from . import b'
    b = importlib.import_module('.b', __package__)

----------
讨论
----------
The problem of manually importing modules with import_module() most commonly
arises when writing code that manipulates or wraps around modules in some way. For
example, perhaps you’re implementing a customized importing mechanism of some
kind where you need to load a module by name and perform patches to the loaded code.


In older code, you will sometimes see the built-in __import__() function used to perform
imports. Although this works, importlib.import_module() is usually easier to
use.

See Recipe 10.11 for an advanced example of customizing the import process.

