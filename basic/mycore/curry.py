# encoding: utf-8
"""
    Topic: sample
    Desc : 
"""
from operator import add, mul
from functools import partial
__author__ = 'Xiong Neng'


def my_curry():
    add1 = partial(add, 1)  # add1(x) = add(1, x)
    mul100 = partial(mul, 100)   # mul100(x) = mul(100, x)
    print(add1(10))
    print(add1(2))
    print(mul100(2))

    # 带关键字参数
    baseTwo = partial(int, base=2)
    baseTwo.__doc__ = 'Convert base 2 string to an int.'
    print(baseTwo('100010'))


if __name__ == '__main__':
    my_curry()


