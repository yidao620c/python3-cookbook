#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
Topic: 给被包装函数增加参数
Desc : 
"""

from functools import wraps
import inspect


def optional_debug(func):
    @wraps(func)
    def wrapper(*args, debug=False, **kwargs):
        if debug:
            print('Calling', func.__name__)
        return func(*args, **kwargs)

    return wrapper


@optional_debug
def spam(a, b, c):
    print(a, b, c)


spam(1, 2, 3)
spam(1, 2, 3, debug=True)


def a(x, debug=False):
    if debug:
        print('Calling a')


def b(x, y, z, debug=False):
    if debug:
        print('Calling b')


def c(x, y, debug=False):
    if debug:
        print('Calling c')


def optional_debug(func):
    if 'debug' in inspect.getargspec(func).args:
        raise TypeError('debug argument already defined')

    @wraps(func)
    def wrapper(*args, debug=False, **kwargs):
        if debug:
            print('Calling', func.__name__)
        return func(*args, **kwargs)

    return wrapper



@optional_debug
def a(x):
    pass


@optional_debug
def b(x, y, z):
    pass


@optional_debug
def c(x, y):
    pass

def optional_debug1(func):
    if 'debug' in inspect.getargspec(func).args:
        raise TypeError('debug argument already defined')

    @wraps(func)
    def wrapper(*args, debug=False, **kwargs):
        if debug:
            print('Calling', func.__name__)
        return func(*args, **kwargs)

    sig = inspect.signature(func)
    parms = list(sig.parameters.values())
    parms.append(inspect.Parameter('debug',
                inspect.Parameter.KEYWORD_ONLY,
                default=False))
    wrapper.__signature__ = sig.replace(parameters=parms)
    return wrapper

@optional_debug1
def add(x,y):
    return x+y

print(inspect.signature(add))

