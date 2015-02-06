#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
Topic: 解除包装器
Desc : 
"""

from functools import wraps

def decorator1(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        print('Decorator 1')
        return func(*args, **kwargs)
    return wrapper

def decorator2(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        print('Decorator 2')
        return func(*args, **kwargs)
    return wrapper

@decorator1
@decorator2
def add(x, y):
    return x + y

add(1, 2)
print('-----------------')
print(add.__wrapped__(2, 3))