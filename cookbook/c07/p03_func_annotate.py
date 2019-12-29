#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
Topic: 函数注解元信息
Desc : 
"""

def add(x:int, y:int) -> int:
    return x + y

help(add)

print(add.__annotations__)

