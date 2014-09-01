#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
    Topic: sample
    Desc : 代码对象
        python提供了大量的BIF来支持可调用/可执行对象，其中包括exec语句
        这些函数帮助程序员执行代码对象，也可以用内建函数compile()生成代码对象
"""
__author__ = 'Xiong Neng'


# compile()函数提供了一次性字节代码预编译，以后每次exec或eval调用都不用编译了
# compile(string, file, type)
# string： 要编译的python代码
# file：   通常被设置为""，代表了存放代码对象的文件名
# type:    代表代码对象的类型，
#   有三个值：eval(和eval一起使用)，single(单一可执行语句，和exec一起使用)，exec
eval_code = compile('100 + 200', '', 'eval')
print(eval(eval_code))
single_code = compile('print "hello, world."', '', 'single')
exec(single_code)
exec_code = compile("""
req = input('Count how many numabers? ')
for eachNum in range(req):
    print(eachNum),
print('================')
""", '', 'exec')
exec(exec_code)

s = input('input a string: ')
print(type(s))
print(s)
exit(1)