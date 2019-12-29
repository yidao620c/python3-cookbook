#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
Topic: 在局部变量域中执行代码
Desc : 
"""

def test3():
    x = 0
    loc = locals()
    print(loc)
    exec('x += 1')
    print(loc)
    locals()
    print(loc)


def test4():
    a = 13
    loc = {'a': a}
    glb = {}
    exec('b = a + 1', glb, loc)
    b = loc['b']
    print(b)
