#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
Topic: 可调整属性的装饰器
Desc : 
"""

from functools import wraps, partial
import logging
import time


# Utility decorator to attach a function as an attribute of obj
def attach_wrapper(obj, func=None):
    if func is None:
        return partial(attach_wrapper, obj)
    setattr(obj, func.__name__, func)
    # return func


def logged(level, name=None, message=None):
    """
    Add logging to a function. level is the logging
    level, name is the logger name, and message is the
    log message. If name and message aren't specified,
    they default to the function's module and name.
    """

    def decorate(func):
        logname = name if name else func.__module__
        log = logging.getLogger(logname)
        logmsg = message if message else func.__name__

        @wraps(func)
        def wrapper(*args, **kwargs):
            log.log(level, logmsg)
            return func(*args, **kwargs)

        # Attach setter functions
        @attach_wrapper(wrapper)
        def set_level(newlevel):
            nonlocal level
            level = newlevel

        @attach_wrapper(wrapper)
        def set_message(newmsg):
            nonlocal logmsg
            logmsg = newmsg

        return wrapper

    return decorate


# Example use
@logged(logging.DEBUG)
def add(x, y):
    return x + y


@logged(logging.CRITICAL, 'example')
def spam():
    print('Spam!')


logging.basicConfig(level=logging.DEBUG)
add(2, 3)
add.set_message('Add called')
add(2, 3)
add.set_level(logging.WARNING)
add(2, 3)

print('---------------------')
spam()
spam.set_message('Add called')
spam()
spam.set_level(logging.WARNING)
spam()


def timethis(func):
    """
    Decorator that reports the execution time.
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(func.__name__, end - start)
        return result

    return wrapper


@logged(logging.DEBUG)
@timethis
def countdown(n):
    while n > 0:
        n -= 1

countdown(10000000)
countdown.set_level(logging.WARNING)
countdown.set_message("Counting down to zero")
countdown(10000000)


@timethis
@logged(logging.DEBUG)
def countdown1(n):
    while n > 0:
        n -= 1

print('****************************************')
countdown1(10000000)
countdown1.set_level(logging.WARNING)
countdown1.set_message("Counting down to zero")
countdown1(10000000)