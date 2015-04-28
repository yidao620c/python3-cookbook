============================
10.2 控制模块被全部导入的内容
============================

----------
问题
----------
You want precise control over the symbols that are exported from a module or package
when a user uses the from module import * statement.

|

----------
解决方案
----------
Define a variable __all__ in your module that explicitly lists the exported names. For
example:

.. code-block:: python

    # somemodule.py
    def spam():
        pass

    def grok():
        pass

    blah = 42
    # Only export 'spam' and 'grok'
    __all__ = ['spam', 'grok']

|

----------
讨论
----------
Although the use of from module import * is strongly discouraged, it still sees frequent
use in modules that define a large number of names. If you don’t do anything, this form
of import will export all names that don’t start with an underscore. On the other hand,
if __all__ is defined, then only the names explicitly listed will be exported.


If you define __all__ as an empty list, then nothing will be exported. An AttributeEr
ror is raised on import if __all__ contains undefined names.

