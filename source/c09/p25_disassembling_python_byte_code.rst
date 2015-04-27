==============================
9.25 拆解Python字节码
==============================

----------
问题
----------
You want to know in detail what your code is doing under the covers by disassembling
it into lower-level byte code used by the interpreter.

|

----------
解决方案
----------
The dis module can be used to output a disassembly of any Python function. For
example:

.. code-block:: python

    >>> def countdown(n):
    ... while n > 0:
    ...     print('T-minus', n)
    ...     n -= 1
    ... print('Blastoff!')
    ...
    >>> import dis
    >>> dis.dis(countdown)
    ...
    >>>

|

----------
讨论
----------
The dis module can be useful if you ever need to study what’s happening in your program
at a very low level (e.g., if you’re trying to understand performance characteristics).
The raw byte code interpreted by the dis() function is available on functions as follows:

.. code-block:: python

    >>> countdown.__code__.co_code
    b"x'\x00|\x00\x00d\x01\x00k\x04\x00r)\x00t\x00\x00d\x02\x00|\x00\x00\x83
    \x02\x00\x01|\x00\x00d\x03\x008}\x00\x00q\x03\x00Wt\x00\x00d\x04\x00\x83
    \x01\x00\x01d\x00\x00S"
    >>>

If you ever want to interpret this code yourself, you would need to use some of the
constants defined in the opcode module. For example:

.. code-block:: python

    >>> c = countdown.__code__.co_code
    >>> import opcode
    >>> opcode.opname[c[0]]
    >>> opcode.opname[c[0]]
    'SETUP_LOOP'
    >>> opcode.opname[c[3]]
    'LOAD_FAST'
    >>>

Ironically, there is no function in the dis module that makes it easy for you to process
the byte code in a programmatic way. However, this generator function will take the raw
byte code sequence and turn it into opcodes and arguments.

.. code-block:: python

    import opcode

    def generate_opcodes(codebytes):
        extended_arg = 0
        i = 0
        n = len(codebytes)
        while i < n:
            op = codebytes[i]
            i += 1
            if op >= opcode.HAVE_ARGUMENT:
                oparg = codebytes[i] + codebytes[i+1]*256 + extended_arg
                extended_arg = 0
                i += 2
                if op == opcode.EXTENDED_ARG:
                    extended_arg = oparg * 65536
                    continue
            else:
                oparg = None
            yield (op, oparg)

To use this function, you would use code like this:

.. code-block:: python

    >>> for op, oparg in generate_opcodes(countdown.__code__.co_code):
    ...     print(op, opcode.opname[op], oparg)

It’s a little-known fact, but you can replace the raw byte code of any function that you
want. It takes a bit of work to do it, but here’s an example of what’s involved:

.. code-block:: python

    >>> def add(x, y):
    ...     return x + y
    ...
    >>> c = add.__code__
    >>> c
    <code object add at 0x1007beed0, file "<stdin>", line 1>
    >>> c.co_code
    b'|\x00\x00|\x01\x00\x17S'
    >>>
    >>> # Make a completely new code object with bogus byte code
    >>> import types
    >>> newbytecode = b'xxxxxxx'
    >>> nc = types.CodeType(c.co_argcount, c.co_kwonlyargcount,
    ...     c.co_nlocals, c.co_stacksize, c.co_flags, newbytecode, c.co_consts,
    ...     c.co_names, c.co_varnames, c.co_filename, c.co_name,
    ...     c.co_firstlineno, c.co_lnotab)
    >>> nc
    <code object add at 0x10069fe40, file "<stdin>", line 1>
    >>> add.__code__ = nc
    >>> add(2,3)
    Segmentation fault

Having the interpreter crash is a pretty likely outcome of pulling a crazy stunt like this.
However, developers working on advanced optimization and metaprogramming tools
might be inclined to rewrite byte code for real. This last part illustrates how to do it. See
`this code on ActiveState <http://code.activestate.com/recipes/277940-decorator-for-bindingconstants-at-compile-time/>`_
for another example of such code in action.


