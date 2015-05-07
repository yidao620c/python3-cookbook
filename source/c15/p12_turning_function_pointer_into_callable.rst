==============================
15.12 将函数指针转换为可调用对象
==============================

----------
问题
----------
You have (somehow) obtained the memory address of a compiled function, but want
to turn it into a Python callable that you can use as an extension function.

Solution
The ctypes module can be used to create Python callables that wrap around arbitrary
memory addresses. The following example shows how to obtain the raw, low-level ad‐
dress of a C function and how to turn it back into a callable object:

>>> import ctypes
>>> lib = ctypes.cdll.LoadLibrary(None)
>>> # Get the address of sin() from the C math library
>>> addr = ctypes.cast(lib.sin, ctypes.c_void_p).value
>>> addr
140735505915760

>>> # Turn the address into a callable function
>>> functype = ctypes.CFUNCTYPE(ctypes.c_double, ctypes.c_double)
>>> func = functype(addr)
>>> func
<CFunctionType object at 0x1006816d0>

>>> # Call the resulting function
>>> func(2)
0.9092974268256817
>>> func(0)
0.0
>>>

Discussion
To make a callable, you must first create a CFUNCTYPE instance. The first argument to
CFUNCTYPE() is the return type. Subsequent arguments are the types of the arguments.
Once you have defined the function type, you wrap it around an integer memory address
to create a callable object. The resulting object is used like any normal function accessed
through ctypes.
This recipe might look rather cryptic and low level. However, it is becoming increasingly
common for programs and libraries to utilize advanced code generation techniques like
just in-time compilation, as found in libraries such as LLVM.
For example, here is a simple example that uses the llvmpy extension to make a small
assembly function, obtain a function pointer to it, and turn it into a Python callable:

>>> from llvm.core import Module, Function, Type, Builder
>>> mod = Module.new('example')
>>> f = Function.new(mod,Type.function(Type.double(), \
                     [Type.double(), Type.double()], False), 'foo')
>>> block = f.append_basic_block('entry')
>>> builder = Builder.new(block)
>>> x2 = builder.fmul(f.args[0],f.args[0])
>>> y2 = builder.fmul(f.args[1],f.args[1])
>>> r = builder.fadd(x2,y2)
>>> builder.ret(r)
<llvm.core.Instruction object at 0x10078e990>
>>> from llvm.ee import ExecutionEngine
>>> engine = ExecutionEngine.new(mod)
>>> ptr = engine.get_pointer_to_function(f)
>>> ptr
4325863440
>>> foo = ctypes.CFUNCTYPE(ctypes.c_double, ctypes.c_double, ctypes.c_double)(ptr)

>>> # Call the resulting function
>>> foo(2,3)
13.0
>>> foo(4,5)
41.0
>>> foo(1,2)
5.0
>>>

It goes without saying that doing anything wrong at this level will probably cause the
Python interpreter to die a horrible death. Keep in mind that you’re directly working
with  machine-level  memory  addresses  and  native  machine  code—not  Python
functions.
