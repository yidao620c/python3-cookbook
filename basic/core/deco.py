# encoding: utf-8
"""
    Topic: sample
    Desc : 利用闭包演示带参的装饰器，错误示范
"""
from time import time

__author__ = 'Xiong Neng'


def logged(when):
    def log(f, *args, **kargs):
        print('Called: function: %s, args: %r, kargs: %r' % (f, args, kargs))

    def pre_logged(f, *args, **kargs):
        log(f, *args, **kargs)
        return f(*args, **kargs)

    def post_logged(f, *args, **kargs):
        now = time()
        try:
            return f(*args, **kargs)
        finally:
            log(f, *args, **kargs)
            print('time delta: %s' % (time() - now))

    try:
        return {'pre': pre_logged, 'post': post_logged}[when]
    except KeyError as e:
        raise ValueError(e, 'must be "pre" or "post"')


@logged('post')
def hello(name):
    print('Hello', name)


hello(*('World!',))


def printparams(a, b, c, d, e=12):
    print((a, b, c, d, e))


def callParams(f):
    return lambda *a, **b: f(*a, **b)


def callParams2(f, *a, **b):
    print('len: ', len(a))
    return f(*a, **b)


callParams(printparams(1, *(2, 3), **{'d': '33', 'e': 333}))
callParams2(printparams, 1, *(2, 3), **{'d': '33', 'e': 333})