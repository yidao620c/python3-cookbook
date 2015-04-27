==============================
9.24 解析与分析Python源码
==============================

----------
问题
----------
You want to write programs that parse and analyze Python source code.

|

----------
解决方案
----------
Most programmers know that Python can evaluate or execute source code provided in
the form of a string. For example:

.. code-block:: python

    >>> x = 42
    >>> eval('2 + 3*4 + x')
    56
    >>> exec('for i in range(10): print(i)')
    0
    1
    2
    3
    4
    5
    6
    7
    8
    9
    >>>

However, the ast module can be used to compile Python source code into an abstract
syntax tree (AST) that can be analyzed. For example:

.. code-block:: python

    >>> import ast
    >>> ex = ast.parse('2 + 3*4 + x', mode='eval')
    >>> ex
    <_ast.Expression object at 0x1007473d0>
    >>> ast.dump(ex)
    "Expression(body=BinOp(left=BinOp(left=Num(n=2), op=Add(),
    right=BinOp(left=Num(n=3), op=Mult(), right=Num(n=4))), op=Add(),
    right=Name(id='x', ctx=Load())))"

    >>> top = ast.parse('for i in range(10): print(i)', mode='exec')
    >>> top
    <_ast.Module object at 0x100747390>
    >>> ast.dump(top)
    "Module(body=[For(target=Name(id='i', ctx=Store()),
    iter=Call(func=Name(id='range', ctx=Load()), args=[Num(n=10)],
    keywords=[], starargs=None, kwargs=None),
    body=[Expr(value=Call(func=Name(id='print', ctx=Load()),
    args=[Name(id='i', ctx=Load())], keywords=[], starargs=None,
    kwargs=None))], orelse=[])])"
    >>>

Analyzing the source tree requires a bit of study on your part, but it consists of a collection
of AST nodes. The easiest way to work with these nodes is to define a visitor
class that implements various visit_NodeName() methods where NodeName() matches
the node of interest. Here is an example of such a class that records information about
which names are loaded, stored, and deleted.

.. code-block:: python

    import ast

    class CodeAnalyzer(ast.NodeVisitor):
        def __init__(self):
            self.loaded = set()
            self.stored = set()
            self.deleted = set()

        def visit_Name(self, node):
            if isinstance(node.ctx, ast.Load):
                self.loaded.add(node.id)
            elif isinstance(node.ctx, ast.Store):
                self.stored.add(node.id)
            elif isinstance(node.ctx, ast.Del):
                self.deleted.add(node.id)

    # Sample usage
    if __name__ == '__main__':
        # Some Python code
        code = '''
        for i in range(10):
            print(i)
        del i
        '''

        # Parse into an AST
        top = ast.parse(code, mode='exec')

        # Feed the AST to analyze name usage
        c = CodeAnalyzer()
        c.visit(top)
        print('Loaded:', c.loaded)
        print('Stored:', c.stored)
        print('Deleted:', c.deleted)

If you run this program, you’ll get output like this:

.. code-block:: python

    Loaded: {'i', 'range', 'print'}
    Stored: {'i'}
    Deleted: {'i'}

Finally, ASTs can be compiled and executed using the compile() function. For example:

.. code-block:: python

    >>> exec(compile(top,'<stdin>', 'exec'))
    0
    1
    2
    3
    4
    5
    6
    7
    8
    9
    >>>

|

----------
讨论
----------
The fact that you can analyze source code and get information from it could be the start
of writing various code analysis, optimization, or verification tools. For instance, instead
of just blindly passing some fragment of code into a function like exec(), you could
turn it into an AST first and look at it in some detail to see what it’s doing. You could
also write tools that look at the entire source code for a module and perform some sort
of static analysis over it.


It should be noted that it is also possible to rewrite the AST to represent new code if you
really know what you’re doing. Here is an example of a decorator that lowers globally
accessed names into the body of a function by reparsing the function body’s source code,
rewriting the AST, and recreating the function’s code object:

.. code-block:: python

    # namelower.py
    import ast
    import inspect

    # Node visitor that lowers globally accessed names into
    # the function body as local variables.
    class NameLower(ast.NodeVisitor):
        def __init__(self, lowered_names):
            self.lowered_names = lowered_names

        def visit_FunctionDef(self, node):
            # Compile some assignments to lower the constants
            code = '__globals = globals()\n'
            code += '\n'.join("{0} = __globals['{0}']".format(name)
                                for name in self.lowered_names)
            code_ast = ast.parse(code, mode='exec')

            # Inject new statements into the function body
            node.body[:0] = code_ast.body

            # Save the function object
            self.func = node

    # Decorator that turns global names into locals
    def lower_names(*namelist):
        def lower(func):
            srclines = inspect.getsource(func).splitlines()
            # Skip source lines prior to the @lower_names decorator
            for n, line in enumerate(srclines):
                if '@lower_names' in line:
                    break

            src = '\n'.join(srclines[n+1:])
            # Hack to deal with indented code
            if src.startswith((' ','\t')):
                src = 'if 1:\n' + src
            top = ast.parse(src, mode='exec')

            # Transform the AST
            cl = NameLower(namelist)
            cl.visit(top)

            # Execute the modified AST
            temp = {}
            exec(compile(top,'','exec'), temp, temp)

            # Pull out the modified code object
            func.__code__ = temp[func.__name__].__code__
            return func
        return lower

To use this code, you would write code such as the following:

.. code-block:: python

    INCR = 1
    @lower_names('INCR')
    def countdown(n):
        while n > 0:
            n -= INCR

The decorator rewrites the source code of the countdown() function to look like this:

.. code-block:: python

    def countdown(n):
        __globals = globals()
        INCR = __globals['INCR']
        while n > 0:
            n -= INCR

In a performance test, it makes the function run about 20% faster.


Now, should you go applying this decorator to all of your functions? Probably not.
However, it’s a good illustration of some very advanced things that might be possible
through AST manipulation, source code manipulation, and other techniques.


This recipe was inspired by a similar recipe at ActiveState that worked by manipulating
Python’s byte code. Working with the AST is a higher-level approach that might be a bit
more straightforward. See the next recipe for more information about byte code.


