==============================
13.2 终止程序并给出错误信息
==============================

----------
问题
----------
You want your program to terminate by printing a message to standard error and re‐
turning a nonzero status code.

|

----------
解决方案
----------
To have a program terminate in this manner, raise a SystemExit exception, but supply
the error message as an argument. For example:

raise SystemExit('It failed!')

This will cause the supplied message to be printed to sys.stderr and the program to
exit with a status code of 1.

|

----------
讨论
----------
This is a small recipe, but it solves a common problem that arises when writing scripts.
Namely, to terminate a program, you might be inclined to write code like this:

import sys
sys.stderr.write('It failed!\n')
raise SystemExit(1)

None of the extra steps involving import or writing to sys.stderr are neccessary if you
simply supply the message to SystemExit() instead.
