================================
10.12 导入模块的同时修改模块
================================

----------
问题
----------
You want to patch or apply decorators to functions in an existing module. However, you
only want to do it if the module actually gets imported and used elsewhere.

----------
解决方案
----------
The essential problem here is that you would like to carry out actions in response to a
module being loaded. Perhaps you want to trigger some kind of callback function that
would notify you when a module was loaded.


This problem can be solved using the same import hook machinery discussed in
Recipe 10.11. Here is a possible solution:

.. code-block:: python

    # postimport.py
    import importlib
    import sys
    from collections import defaultdict

    _post_import_hooks = defaultdict(list)

    class PostImportFinder:
        def __init__(self):
            self._skip = set()

        def find_module(self, fullname, path=None):
            if fullname in self._skip:
                return None
            self._skip.add(fullname)
            return PostImportLoader(self)

    class PostImportLoader:
        def __init__(self, finder):
            self._finder = finder

        def load_module(self, fullname):
            importlib.import_module(fullname)
            module = sys.modules[fullname]
            for func in _post_import_hooks[fullname]:
                func(module)
            self._finder._skip.remove(fullname)
            return module

    def when_imported(fullname):
        def decorate(func):
            if fullname in sys.modules:
                func(sys.modules[fullname])
            else:
                _post_import_hooks[fullname].append(func)
            return func
        return decorate

    sys.meta_path.insert(0, PostImportFinder())

To use this code, you use the when_imported() decorator. For example:

.. code-block:: python

    >>> from postimport import when_imported
    >>> @when_imported('threading')
    ... def warn_threads(mod):
    ...     print('Threads? Are you crazy?')
    ...
    >>>
    >>> import threading
    Threads? Are you crazy?
    >>>

As a more practical example, maybe you want to apply decorators to existing definitions,
such as shown here:

.. code-block:: python

    from functools import wraps
    from postimport import when_imported

    def logged(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            print('Calling', func.__name__, args, kwargs)
            return func(*args, **kwargs)
        return wrapper

    # Example
    @when_imported('math')
    def add_logging(mod):
        mod.cos = logged(mod.cos)
        mod.sin = logged(mod.sin)

----------
讨论
----------
This recipe relies on the import hooks that were discussed in Recipe 10.11, with a slight
twist.


First, the role of the @when_imported decorator is to register handler functions that get
triggered on import. The decorator checks sys.modules to see if a module was already
loaded. If so, the handler is invoked immediately. Otherwise, the handler is added to a
list in the _post_import_hooks dictionary. The purpose of _post_import_hooks is
simply to collect all handler objects that have been registered for each module. In principle,
more than one handler could be registered for a given module.


To trigger the pending actions in _post_import_hooks after module import, the Post
ImportFinder class is installed as the first item in sys.meta_path. If you recall from
Recipe 10.11, sys.meta_path contains a list of finder objects that are consulted in order
to locate modules. By installing PostImportFinder as the first item, it captures all module
imports.


In this recipe, however, the role of PostImportFinder is not to load modules, but to
trigger actions upon the completion of an import. To do this, the actual import is delegated
to the other finders on sys.meta_path. Rather than trying to do this directly, the
function imp.import_module() is called recursively in the PostImportLoader class. To
avoid getting stuck in an infinite loop, PostImportFinder keeps a set of all the modules
that are currently in the process of being loaded. If a module name is part of this set, it
is simply ignored by PostImportFinder. This is what causes the import request to pass
to the other finders on sys.meta_path.

After a module has been loaded with imp.import_module(), all handlers currently registered
in _post_import_hooks are called with the newly loaded module as an argument.


From this point forward, the handlers are free to do what they want with the module.
A major feature of the approach shown in this recipe is that the patching of a module
occurs in a seamless fashion, regardless of where or how a module of interest is actually
loaded. You simply write a handler function that’s decorated with @when_imported()
and it all just magically works from that point forward.


One caution about this recipe is that it does not work for modules that have been explicitly
reloaded using imp.reload(). That is, if you reload a previously loaded module,
the post import handler function doesn’t get triggered again (all the more reason to not
use reload() in production code). On the other hand, if you delete the module from
sys.modules and redo the import, you’ll see the handler trigger again.


More information about post-import hooks can be found in PEP 369 . As of this writing,
the PEP has been withdrawn by the author due to it being out of date with the current
implementation of the importlib module. However, it is easy enough to implement
your own solution using this recipe.
