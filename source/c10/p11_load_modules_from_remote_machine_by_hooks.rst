================================
10.11 通过导入钩子远程加载模块
================================

----------
问题
----------
你想自定义Python的import语句，使得它能从远程机器上面透明的加载模块。

----------
解决方案
----------
首先要提出来的是安全问题。本届讨论的思想如果没有一些额外的安全和认知机制的话会很糟糕。
也就是说，我们的主要目的是深入分析Python的import语句机制。
如果你理解了本节内部原理，你就能够为其他任何目的而自定义import。
有了这些，让我们继续向前走。

本节核心是设计导入语句的扩展功能。有很多种方法可以做这个，
不过为了演示的方便，我们开始先构造下面这个Python代码结构：

::

    testcode/
        spam.py
        fib.py
        grok/
            __init__.py
            blah.py

这些文件的内容并不重要，不过我们在每个文件中放入了少量的简单语句和函数，
这样你可以测试它们并查看当它们被导入时的输出。例如：

.. code-block:: python

    # spam.py
    print("I'm spam")

    def hello(name):
        print('Hello %s' % name)

    # fib.py
    print("I'm fib")

    def fib(n):
        if n < 2:
            return 1
        else:
            return fib(n-1) + fib(n-2)

    # grok/__init__.py
    print("I'm grok.__init__")

    # grok/blah.py
    print("I'm grok.blah")

这里的目的是允许这些文件作为模块被远程访问。
也许最简单的方式就是将它们发布到一个web服务器上面。在testcode目录中像下面这样运行Python：

::

    bash % cd testcode
    bash % python3 -m http.server 15000
    Serving HTTP on 0.0.0.0 port 15000 ...

Leave that server running and start up a separate Python interpreter. Make sure you can
access the remote files using urllib. For example:


.. code-block:: python

    >>> from urllib.request import urlopen
    >>> u = urlopen('http://localhost:15000/fib.py')
    >>> data = u.read().decode('utf-8')
    >>> print(data)
    # fib.py
    print("I'm fib")

    def fib(n):
        if n < 2:
            return 1
        else:
            return fib(n-1) + fib(n-2)
    >>>

Loading source code from this server is going to form the basis for the remainder of
this recipe. Specifically, instead of manually grabbing a file of source code using urlop
en(), the import statement will be customized to do it transparently behind the scenes.


The first approach to loading a remote module is to create an explicit loading function
for doing it. For example:

.. code-block:: python

    import imp
    import urllib.request
    import sys

    def load_module(url):
        u = urllib.request.urlopen(url)
        source = u.read().decode('utf-8')
        mod = sys.modules.setdefault(url, imp.new_module(url))
        code = compile(source, url, 'exec')
        mod.__file__ = url
        mod.__package__ = ''
        exec(code, mod.__dict__)
        return mod

This function merely downloads the source code, compiles it into a code object using
compile(), and executes it in the dictionary of a newly created module object. Here’s
how you would use the function:

.. code-block:: python

    >>> fib = load_module('http://localhost:15000/fib.py')
    I'm fib
    >>> fib.fib(10)
    89
    >>> spam = load_module('http://localhost:15000/spam.py')
    I'm spam
    >>> spam.hello('Guido')
    Hello Guido
    >>> fib
    <module 'http://localhost:15000/fib.py' from 'http://localhost:15000/fib.py'>
    >>> spam
    <module 'http://localhost:15000/spam.py' from 'http://localhost:15000/spam.py'>
    >>>

As you can see, it “works” for simple modules. However, it’s not plugged into the usual
import statement, and extending the code to support more advanced constructs, such
as packages, would require additional work.

A much slicker approach is to create a custom importer. The first way to do this is to
create what’s known as a meta path importer. Here is an example:

.. code-block:: python

    # urlimport.py
    import sys
    import importlib.abc
    import imp
    from urllib.request import urlopen
    from urllib.error import HTTPError, URLError
    from html.parser import HTMLParser

    # Debugging
    import logging
    log = logging.getLogger(__name__)

    # Get links from a given URL
    def _get_links(url):
        class LinkParser(HTMLParser):
            def handle_starttag(self, tag, attrs):
                if tag == 'a':
                    attrs = dict(attrs)
                    links.add(attrs.get('href').rstrip('/'))
        links = set()
        try:
            log.debug('Getting links from %s' % url)
            u = urlopen(url)
            parser = LinkParser()
            parser.feed(u.read().decode('utf-8'))
        except Exception as e:
            log.debug('Could not get links. %s', e)
        log.debug('links: %r', links)
        return links

    class UrlMetaFinder(importlib.abc.MetaPathFinder):
        def __init__(self, baseurl):
            self._baseurl = baseurl
            self._links = { }
            self._loaders = { baseurl : UrlModuleLoader(baseurl) }

        def find_module(self, fullname, path=None):
            log.debug('find_module: fullname=%r, path=%r', fullname, path)
            if path is None:
                baseurl = self._baseurl
            else:
                if not path[0].startswith(self._baseurl):
                    return None
                baseurl = path[0]
            parts = fullname.split('.')
            basename = parts[-1]
            log.debug('find_module: baseurl=%r, basename=%r', baseurl, basename)

            # Check link cache
            if basename not in self._links:
                self._links[baseurl] = _get_links(baseurl)

            # Check if it's a package
            if basename in self._links[baseurl]:
                log.debug('find_module: trying package %r', fullname)
                fullurl = self._baseurl + '/' + basename
                # Attempt to load the package (which accesses __init__.py)
                loader = UrlPackageLoader(fullurl)
                try:
                    loader.load_module(fullname)
                    self._links[fullurl] = _get_links(fullurl)
                    self._loaders[fullurl] = UrlModuleLoader(fullurl)
                    log.debug('find_module: package %r loaded', fullname)
                except ImportError as e:
                    log.debug('find_module: package failed. %s', e)
                    loader = None
                return loader
            # A normal module
            filename = basename + '.py'
            if filename in self._links[baseurl]:
                log.debug('find_module: module %r found', fullname)
                return self._loaders[baseurl]
            else:
                log.debug('find_module: module %r not found', fullname)
                return None

        def invalidate_caches(self):
            log.debug('invalidating link cache')
            self._links.clear()

    # Module Loader for a URL
    class UrlModuleLoader(importlib.abc.SourceLoader):
        def __init__(self, baseurl):
            self._baseurl = baseurl
            self._source_cache = {}

        def module_repr(self, module):
            return '<urlmodule %r from %r>' % (module.__name__, module.__file__)

        # Required method
        def load_module(self, fullname):
            code = self.get_code(fullname)
            mod = sys.modules.setdefault(fullname, imp.new_module(fullname))
            mod.__file__ = self.get_filename(fullname)
            mod.__loader__ = self
            mod.__package__ = fullname.rpartition('.')[0]
            exec(code, mod.__dict__)
            return mod

        # Optional extensions
        def get_code(self, fullname):
            src = self.get_source(fullname)
            return compile(src, self.get_filename(fullname), 'exec')

        def get_data(self, path):
            pass

        def get_filename(self, fullname):
            return self._baseurl + '/' + fullname.split('.')[-1] + '.py'

        def get_source(self, fullname):
            filename = self.get_filename(fullname)
            log.debug('loader: reading %r', filename)
            if filename in self._source_cache:
                log.debug('loader: cached %r', filename)
                return self._source_cache[filename]
            try:
                u = urlopen(filename)
                source = u.read().decode('utf-8')
                log.debug('loader: %r loaded', filename)
                self._source_cache[filename] = source
                return source
            except (HTTPError, URLError) as e:
                log.debug('loader: %r failed. %s', filename, e)
                raise ImportError("Can't load %s" % filename)

        def is_package(self, fullname):
            return False

    # Package loader for a URL
    class UrlPackageLoader(UrlModuleLoader):
        def load_module(self, fullname):
            mod = super().load_module(fullname)
            mod.__path__ = [ self._baseurl ]
            mod.__package__ = fullname

        def get_filename(self, fullname):
            return self._baseurl + '/' + '__init__.py'

        def is_package(self, fullname):
            return True

    # Utility functions for installing/uninstalling the loader
    _installed_meta_cache = { }
    def install_meta(address):
        if address not in _installed_meta_cache:
            finder = UrlMetaFinder(address)
            _installed_meta_cache[address] = finder
            sys.meta_path.append(finder)
            log.debug('%r installed on sys.meta_path', finder)

    def remove_meta(address):
        if address in _installed_meta_cache:
            finder = _installed_meta_cache.pop(address)
            sys.meta_path.remove(finder)
            log.debug('%r removed from sys.meta_path', finder)

Here is an interactive session showing how to use the preceding code:

.. code-block:: python

    >>> # importing currently fails
    >>> import fib
    Traceback (most recent call last):
    File "<stdin>", line 1, in <module>
    ImportError: No module named 'fib'
    >>> # Load the importer and retry (it works)
    >>> import urlimport
    >>> urlimport.install_meta('http://localhost:15000')
    >>> import fib
    I'm fib
    >>> import spam
    I'm spam
    >>> import grok.blah
    I'm grok.__init__
    I'm grok.blah
    >>> grok.blah.__file__
    'http://localhost:15000/grok/blah.py'
    >>>

This particular solution involves installing an instance of a special finder object UrlMe
taFinder as the last entry in sys.meta_path. Whenever modules are imported, the
finders in sys.meta_path are consulted in order to locate the module. In this example,
the UrlMetaFinder instance becomes a finder of last resort that’s triggered when a
module can’t be found in any of the normal locations.


As for the general implementation approach, the UrlMetaFinder class wraps around a
user-specified URL. Internally, the finder builds sets of valid links by scraping them
from the given URL. When imports are made, the module name is compared against
this set of known links. If a match can be found, a separate UrlModuleLoader class is
used to load source code from the remote machine and create the resulting module
object. One reason for caching the links is to avoid unnecessary HTTP requests on
repeated imports.


The second approach to customizing import is to write a hook that plugs directly into
the sys.path variable, recognizing certain directory naming patterns. Add the following
class and support functions to urlimport.py:

.. code-block:: python

    # urlimport.py
    # ... include previous code above ...
    # Path finder class for a URL
    class UrlPathFinder(importlib.abc.PathEntryFinder):
        def __init__(self, baseurl):
            self._links = None
            self._loader = UrlModuleLoader(baseurl)
            self._baseurl = baseurl

        def find_loader(self, fullname):
            log.debug('find_loader: %r', fullname)
            parts = fullname.split('.')
            basename = parts[-1]
            # Check link cache
            if self._links is None:
                self._links = [] # See discussion
                self._links = _get_links(self._baseurl)

            # Check if it's a package
            if basename in self._links:
                log.debug('find_loader: trying package %r', fullname)
                fullurl = self._baseurl + '/' + basename
                # Attempt to load the package (which accesses __init__.py)
                loader = UrlPackageLoader(fullurl)
                try:
                    loader.load_module(fullname)
                    log.debug('find_loader: package %r loaded', fullname)
                except ImportError as e:
                    log.debug('find_loader: %r is a namespace package', fullname)
                    loader = None
                return (loader, [fullurl])

            # A normal module
            filename = basename + '.py'
            if filename in self._links:
                log.debug('find_loader: module %r found', fullname)
                return (self._loader, [])
            else:
                log.debug('find_loader: module %r not found', fullname)
                return (None, [])

        def invalidate_caches(self):
            log.debug('invalidating link cache')
            self._links = None

    # Check path to see if it looks like a URL
    _url_path_cache = {}
    def handle_url(path):
        if path.startswith(('http://', 'https://')):
            log.debug('Handle path? %s. [Yes]', path)
            if path in _url_path_cache:
                finder = _url_path_cache[path]
            else:
                finder = UrlPathFinder(path)
                _url_path_cache[path] = finder
            return finder
        else:
            log.debug('Handle path? %s. [No]', path)

    def install_path_hook():
        sys.path_hooks.append(handle_url)
        sys.path_importer_cache.clear()
        log.debug('Installing handle_url')

    def remove_path_hook():
        sys.path_hooks.remove(handle_url)
        sys.path_importer_cache.clear()
        log.debug('Removing handle_url')

To use this path-based finder, you simply add URLs to sys.path. For example:

.. code-block:: python

    >>> # Initial import fails
    >>> import fib
    Traceback (most recent call last):
        File "<stdin>", line 1, in <module>
    ImportError: No module named 'fib'

    >>> # Install the path hook
    >>> import urlimport
    >>> urlimport.install_path_hook()

    >>> # Imports still fail (not on path)
    >>> import fib
    Traceback (most recent call last):
        File "<stdin>", line 1, in <module>
    ImportError: No module named 'fib'

    >>> # Add an entry to sys.path and watch it work
    >>> import sys
    >>> sys.path.append('http://localhost:15000')
    >>> import fib
    I'm fib
    >>> import grok.blah
    I'm grok.__init__
    I'm grok.blah
    >>> grok.blah.__file__
    'http://localhost:15000/grok/blah.py'
    >>>

The key to this last example is the handle_url() function, which is added to the
sys.path_hooks variable. When the entries on sys.path are being processed, the functions
in sys.path_hooks are invoked. If any of those functions return a finder object,
that finder is used to try to load modules for that entry on sys.path.


It should be noted that the remotely imported modules work exactly like any other
module. For instance:

.. code-block:: python

    >>> fib
    <urlmodule 'fib' from 'http://localhost:15000/fib.py'>
    >>> fib.__name__
    'fib'
    >>> fib.__file__
    'http://localhost:15000/fib.py'
    >>> import inspect
    >>> print(inspect.getsource(fib))
    # fib.py
    print("I'm fib")

    def fib(n):
        if n < 2:
            return 1
        else:
            return fib(n-1) + fib(n-2)
    >>>

----------
讨论
----------
Before discussing this recipe in further detail, it should be emphasized that Python’s
module, package, and import mechanism is one of the most complicated parts of the
entire language—often poorly understood by even the most seasoned Python programmers
unless they’ve devoted effort to peeling back the covers. There are several
critical documents that are worth reading, including the documentation for the
`importlib module <https://docs.python.org/3/library/importlib.html>`_
and `PEP 302 <http://www.python.org/dev/peps/pep-0302>`_.
That documentation won’t be repeated here, but some
essential highlights will be discussed.

First, if you want to create a new module object, you use the imp.new_module() function.
For example:

.. code-block:: python

    >>> import imp
    >>> m = imp.new_module('spam')
    >>> m
    <module 'spam'>
    >>> m.__name__
    'spam'
    >>>

Module objects usually have a few expected attributes, including __file__ (the name
of the file that the module was loaded from) and __package__ (the name of the enclosing
package, if any).


Second, modules are cached by the interpreter. The module cache can be found in the
dictionary sys.modules. Because of this caching, it’s common to combine caching and
module creation together into a single step. For example:

.. code-block:: python

    >>> import sys
    >>> import imp
    >>> m = sys.modules.setdefault('spam', imp.new_module('spam'))
    >>> m
    <module 'spam'>
    >>>

The main reason for doing this is that if a module with the given name already exists,
you’ll get the already created module instead. For example:

.. code-block:: python

    >>> import math
    >>> m = sys.modules.setdefault('math', imp.new_module('math'))
    >>> m
    <module 'math' from '/usr/local/lib/python3.3/lib-dynload/math.so'>
    >>> m.sin(2)
    0.9092974268256817
    >>> m.cos(2)
    -0.4161468365471424
    >>>

Since creating modules is easy, it is straightforward to write simple functions, such as
the load_module() function in the first part of this recipe. A downside of this approach
is that it is actually rather tricky to handle more complicated cases, such as package
imports. In order to handle a package, you would have to reimplement much of the
underlying logic that’s already part of the normal import statement (e.g., checking for
directories, looking for __init__.py files, executing those files, setting up paths, etc.).
This complexity is one of the reasons why it’s often better to extend the import statement
directly rather than defining a custom function.


Extending the import statement is straightforward, but involves a number of moving
parts. At the highest level, import operations are processed by a list of “meta-path”
finders that you can find in the list sys.meta_path. If you output its value, you’ll see
the following:

.. code-block:: python

    >>> from pprint import pprint
    >>> pprint(sys.meta_path)
    [<class '_frozen_importlib.BuiltinImporter'>,
    <class '_frozen_importlib.FrozenImporter'>,
    <class '_frozen_importlib.PathFinder'>]
    >>>

When executing a statement such as import fib, the interpreter walks through the
finder objects on sys.meta_path and invokes their find_module() method in order to
locate an appropriate module loader. It helps to see this by experimentation, so define
the following class and try the following:

.. code-block:: python

    >>> class Finder:
    ...     def find_module(self, fullname, path):
    ...         print('Looking for', fullname, path)
    ...         return None
    ...
    >>> import sys
    >>> sys.meta_path.insert(0, Finder()) # Insert as first entry
    >>> import math
    Looking for math None
    >>> import types
    Looking for types None
    >>> import threading
    Looking for threading None
    Looking for time None
    Looking for traceback None
    Looking for linecache None
    Looking for tokenize None
    Looking for token None
    >>>

Notice how the find_module() method is being triggered on every import. The role of
the path argument in this method is to handle packages. When packages are imported,
it is a list of the directories that are found in the package’s __path__ attribute. These are
the paths that need to be checked to find package subcomponents. For example, notice
the path setting for xml.etree and xml.etree.ElementTree:

.. code-block:: python

    >>> import xml.etree.ElementTree
    Looking for xml None
    Looking for xml.etree ['/usr/local/lib/python3.3/xml']
    Looking for xml.etree.ElementTree ['/usr/local/lib/python3.3/xml/etree']
    Looking for warnings None
    Looking for contextlib None
    Looking for xml.etree.ElementPath ['/usr/local/lib/python3.3/xml/etree']
    Looking for _elementtree None
    Looking for copy None
    Looking for org None
    Looking for pyexpat None
    Looking for ElementC14N None
    >>>

The placement of the finder on sys.meta_path is critical. Remove it from the front of
the list to the end of the list and try more imports:

.. code-block:: python

    >>> del sys.meta_path[0]
    >>> sys.meta_path.append(Finder())
    >>> import urllib.request
    >>> import datetime

Now you don’t see any output because the imports are being handled by other entries
in sys.meta_path. In this case, you would only see it trigger when nonexistent modules
are imported:

.. code-block:: python

    >>> import fib
    Looking for fib None
    Traceback (most recent call last):
        File "<stdin>", line 1, in <module>
    ImportError: No module named 'fib'
    >>> import xml.superfast
    Looking for xml.superfast ['/usr/local/lib/python3.3/xml']
    Traceback (most recent call last):
        File "<stdin>", line 1, in <module>
    ImportError: No module named 'xml.superfast'
    >>>

The fact that you can install a finder to catch unknown modules is the key to the
UrlMetaFinder class in this recipe. An instance of UrlMetaFinder is added to the end
of sys.meta_path, where it serves as a kind of importer of last resort. If the requested
module name can’t be located by any of the other import mechanisms, it gets handled
by this finder. Some care needs to be taken when handling packages. Specifically, the
value presented in the path argument needs to be checked to see if it starts with the URL
registered in the finder. If not, the submodule must belong to some other finder and
should be ignored.


Additional handling of packages is found in the UrlPackageLoader class. This class,
rather than importing the package name, tries to load the underlying __init__.py file.
It also sets the module __path__ attribute. This last part is critical, as the value set will
be passed to subsequent find_module() calls when loading package submodules.
The path-based import hook is an extension of these ideas, but based on a somewhat
different mechanism. As you know, sys.path is a list of directories where Python looks
for modules. For example:

.. code-block:: python

    >>> from pprint import pprint
    >>> import sys
    >>> pprint(sys.path)
    ['',
    '/usr/local/lib/python33.zip',
    '/usr/local/lib/python3.3',
    '/usr/local/lib/python3.3/plat-darwin',
    '/usr/local/lib/python3.3/lib-dynload',
    '/usr/local/lib/...3.3/site-packages']
    >>>

Each entry in sys.path is additionally attached to a finder object. You can view these
finders by looking at sys.path_importer_cache:

.. code-block:: python

    >>> pprint(sys.path_importer_cache)
    {'.': FileFinder('.'),
    '/usr/local/lib/python3.3': FileFinder('/usr/local/lib/python3.3'),
    '/usr/local/lib/python3.3/': FileFinder('/usr/local/lib/python3.3/'),
    '/usr/local/lib/python3.3/collections': FileFinder('...python3.3/collections'),
    '/usr/local/lib/python3.3/encodings': FileFinder('...python3.3/encodings'),
    '/usr/local/lib/python3.3/lib-dynload': FileFinder('...python3.3/lib-dynload'),
    '/usr/local/lib/python3.3/plat-darwin': FileFinder('...python3.3/plat-darwin'),
    '/usr/local/lib/python3.3/site-packages': FileFinder('...python3.3/site-packages'),
    '/usr/local/lib/python33.zip': None}
    >>>

sys.path_importer_cache tends to be much larger than sys.path because it records
finders for all known directories where code is being loaded. This includes subdirectories
of packages which usually aren’t included on sys.path.


To execute import fib, the directories on sys.path are checked in order. For each
directory, the name fib is presented to the associated finder found in sys.path_im
porter_cache. This is also something that you can investigate by making your own
finder and putting an entry in the cache. Try this experiment:

.. code-block:: python

    >>> class Finder:
    ... def find_loader(self, name):
    ...     print('Looking for', name)
    ...     return (None, [])
    ...
    >>> import sys
    >>> # Add a "debug" entry to the importer cache
    >>> sys.path_importer_cache['debug'] = Finder()
    >>> # Add a "debug" directory to sys.path
    >>> sys.path.insert(0, 'debug')
    >>> import threading
    Looking for threading
    Looking for time
    Looking for traceback
    Looking for linecache
    Looking for tokenize
    Looking for token
    >>>

Here, you’ve installed a new cache entry for the name debug and installed the name
debug as the first entry on sys.path. On all subsequent imports, you see your finder
being triggered. However, since it returns (None, []), processing simply continues to the
next entry.


The population of sys.path_importer_cache is controlled by a list of functions stored
in sys.path_hooks. Try this experiment, which clears the cache and adds a new path
checking function to sys.path_hooks:

.. code-block:: python

    >>> sys.path_importer_cache.clear()
    >>> def check_path(path):
    ...     print('Checking', path)
    ...     raise ImportError()
    ...
    >>> sys.path_hooks.insert(0, check_path)
    >>> import fib
    Checked debug
    Checking .
    Checking /usr/local/lib/python33.zip
    Checking /usr/local/lib/python3.3
    Checking /usr/local/lib/python3.3/plat-darwin
    Checking /usr/local/lib/python3.3/lib-dynload
    Checking /Users/beazley/.local/lib/python3.3/site-packages
    Checking /usr/local/lib/python3.3/site-packages
    Looking for fib
    Traceback (most recent call last):
        File "<stdin>", line 1, in <module>
    ImportError: No module named 'fib'
    >>>

As you can see, the check_path() function is being invoked for every entry on
sys.path. However, since an ImportError exception is raised, nothing else happens
(checking just moves to the next function on sys.path_hooks).


Using this knowledge of how sys.path is processed, you can install a custom path
checking function that looks for filename patterns, such as URLs. For instance:

.. code-block:: python

    >>> def check_url(path):
    ...     if path.startswith('http://'):
    ...         return Finder()
    ...     else:
    ...         raise ImportError()
    ...
    >>> sys.path.append('http://localhost:15000')
    >>> sys.path_hooks[0] = check_url
    >>> import fib
    Looking for fib # Finder output!
    Traceback (most recent call last):
        File "<stdin>", line 1, in <module>
    ImportError: No module named 'fib'

    >>> # Notice installation of Finder in sys.path_importer_cache
    >>> sys.path_importer_cache['http://localhost:15000']
    <__main__.Finder object at 0x10064c850>
    >>>

This is the key mechanism at work in the last part of this recipe. Essentially, a custom
path checking function has been installed that looks for URLs in sys.path. When they
are encountered, a new UrlPathFinder instance is created and installed into
sys.path_importer_cache. From that point forward, all import statements that pass
through that part of sys.path will try to use your custom finder.


Package handling with a path-based importer is somewhat tricky, and relates to the
return value of the find_loader() method. For simple modules, find_loader() returns
a tuple (loader, None) where loader is an instance of a loader that will import
the module.


For a normal package, find_loader() returns a tuple (loader, path) where loader
is the loader instance that will import the package (and execute __init__.py) and path
is a list of the directories that will make up the initial setting of the package’s __path__
attribute. For example, if the base URL was http://localhost:15000 and a user executed
import grok, the path returned by find_loader() would be [ 'http://local
host:15000/grok' ].


The find_loader() must additionally account for the possibility of a namespace package.
A namespace package is a package where a valid package directory name exists,
but no __init__.py file can be found. For this case, find_loader() must return a tuple
(None, path) where path is a list of directories that would have made up the package’s
__path__ attribute had it defined an __init__.py file. For this case, the import mechanism
moves on to check further directories on sys.path. If more namespace packages
are found, all of the resulting paths are joined together to make a final namespace package.
See Recipe 10.5 for more information on namespace packages.


There is a recursive element to package handling that is not immediately obvious in the
solution, but also at work. All packages contain an internal path setting, which can be
found in __path__ attribute. For example:

.. code-block:: python

    >>> import xml.etree.ElementTree
    >>> xml.__path__
    ['/usr/local/lib/python3.3/xml']
    >>> xml.etree.__path__
    ['/usr/local/lib/python3.3/xml/etree']
    >>>

As mentioned, the setting of __path__ is controlled by the return value of the find_load
er() method. However, the subsequent processing of __path__ is also handled by the
functions in sys.path_hooks. Thus, when package subcomponents are loaded, the entries
in __path__ are checked by the handle_url() function. This causes new instances
of UrlPathFinder to be created and added to sys.path_importer_cache.


One remaining tricky part of the implementation concerns the behavior of the han
dle_url() function and its interaction with the _get_links() function used internally.
If your implementation of a finder involves the use of other modules (e.g., urllib.re
quest), there is a possibility that those modules will attempt to make further imports
in the middle of the finder’s operation. This can actually cause handle_url() and other
parts of the finder to get executed in a kind of recursive loop. To account for this possibility,
the implementation maintains a cache of created finders (one per URL). This
avoids the problem of creating duplicate finders. In addition, the following fragment of
code ensures that the finder doesn’t respond to any import requests while it’s in the
processs of getting the initial set of links:

.. code-block:: python

    # Check link cache
    if self._links is None:
        self._links = [] # See discussion
        self._links = _get_links(self._baseurl)

You may not need this checking in other implementations, but for this example involving
URLs, it was required.


Finally, the invalidate_caches() method of both finders is a utility method that is
supposed to clear internal caches should the source code change. This method is triggered
when a user invokes importlib.invalidate_caches(). You might use it if you
want the URL importers to reread the list of links, possibly for the purpose of being able
to access newly added files.


In comparing the two approaches (modifying sys.meta_path or using a path hook), it
helps to take a high-level view. Importers installed using sys.meta_path are free to
handle modules in any manner that they wish. For instance, they could load modules
out of a database or import them in a manner that is radically different than normal
module/package handling. This freedom also means that such importers need to do
more bookkeeping and internal management. This explains, for instance, why the implementation
of UrlMetaFinder needs to do its own caching of links, loaders, and other
details. On the other hand, path-based hooks are more narrowly tied to the processing
of sys.path. Because of the connection to sys.path, modules loaded with such extensions
will tend to have the same features as normal modules and packages that programmers
are used to.

Assuming that your head hasn’t completely exploded at this point, a key to understanding
and experimenting with this recipe may be the added logging calls. You can enable
logging and try experiments such as this:

.. code-block:: python

    >>> import logging
    >>> logging.basicConfig(level=logging.DEBUG)
    >>> import urlimport
    >>> urlimport.install_path_hook()
    DEBUG:urlimport:Installing handle_url
    >>> import fib
    DEBUG:urlimport:Handle path? /usr/local/lib/python33.zip. [No]
    Traceback (most recent call last):
    File "<stdin>", line 1, in <module>
    ImportError: No module named 'fib'
    >>> import sys
    >>> sys.path.append('http://localhost:15000')
    >>> import fib
    DEBUG:urlimport:Handle path? http://localhost:15000. [Yes]
    DEBUG:urlimport:Getting links from http://localhost:15000
    DEBUG:urlimport:links: {'spam.py', 'fib.py', 'grok'}
    DEBUG:urlimport:find_loader: 'fib'
    DEBUG:urlimport:find_loader: module 'fib' found
    DEBUG:urlimport:loader: reading 'http://localhost:15000/fib.py'
    DEBUG:urlimport:loader: 'http://localhost:15000/fib.py' loaded
    I'm fib
    >>>

Last, but not least, spending some time sleeping with
`PEP 302 <http://www.python.org/dev/peps/pep-0302>`_ and the documentation
for importlib under your pillow may be advisable.
