================================
10.14 创建新的Python环境
================================

----------
问题
----------
You want to create a new Python environment in which you can install modules and
packages. However, you want to do this without installing a new copy of Python or
making changes that might affect the system Python installation.

----------
解决方案
----------
You can make a new “virtual” environment using the pyvenv command. This command
is installed in the same directory as the Python interpreter or possibly in the Scripts
directory on Windows. Here is an example:

.. code-block:: python

    bash % pyvenv Spam
    bash %

The name supplied to pyvenv is the name of a directory that will be created. Upon
creation, the Spam directory will look something like this:

.. code-block:: python

    bash % cd Spam
    bash % ls
    bin include lib pyvenv.cfg
    bash %

In the bin directory, you’ll find a Python interpreter that you can use. For example:

.. code-block:: python

    bash % Spam/bin/python3
    Python 3.3.0 (default, Oct 6 2012, 15:45:22)
    [GCC 4.2.1 (Apple Inc. build 5666) (dot 3)] on darwin
    Type "help", "copyright", "credits" or "license" for more information.
    >>> from pprint import pprint
    >>> import sys
    >>> pprint(sys.path)
    ['',
    '/usr/local/lib/python33.zip',
    '/usr/local/lib/python3.3',
    '/usr/local/lib/python3.3/plat-darwin',
    '/usr/local/lib/python3.3/lib-dynload',
    '/Users/beazley/Spam/lib/python3.3/site-packages']
    >>>

A key feature of this interpreter is that its site-packages directory has been set to the
newly created environment. Should you decide to install third-party packages, they will
be installed here, not in the normal system site-packages directory.

----------
讨论
----------
The creation of a virtual environment mostly pertains to the installation and management
of third-party packages. As you can see in the example, the sys.path variable
contains directories from the normal system Python, but the site-packages directory has
been relocated to a new directory.


With a new virtual environment, the next step is often to install a package manager,
such as distribute or pip. When installing such tools and subsequent packages, you
just need to make sure you use the interpreter that’s part of the virtual environment.
This should install the packages into the newly created site-packages directory.


Although a virtual environment might look like a copy of the Python installation, it
really only consists of a few files and symbolic links. All of the standard library files and
interpreter executables come from the original Python installation. Thus, creating such
environments is easy, and takes almost no machine resources.


By default, virtual environments are completely clean and contain no third-party addons.
If you would like to include already installed packages as part of a virtual environment,
create the environment using the --system-site-packages option. For example:

.. code-block:: python

    bash % pyvenv --system-site-packages Spam
    bash %

More information about pyvenv and virtual environments can be found in
`PEP 405 <https://www.python.org/dev/peps/pep-0405/>`_.


