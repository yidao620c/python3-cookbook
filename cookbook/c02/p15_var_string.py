#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
Topic: 字符串中的变量
Desc : 
"""
import sys

class Info:
    def __init__(self, name, n):
        self.name = name
        self.n = n


class SafeSub(dict):
    """防止key找不到"""
    def __missing__(self, key):
        return '{' + key + '}'


def sub(text):
    return text.format_map(SafeSub(sys._getframe(1).f_locals))

def var_str():
    s = '{name} has {n} messages.'
    print(s.format(name='Guido', n=37))

    # vars()和format_map
    a = Info('Guido', 37)
    print(s.format_map(vars(a)))

    name = 'Lisi'
    print(s.format_map(SafeSub(vars())))

    name = 'Guido'
    n = 37
    print(sub('Hello {name}'))
    print(sub('You have {n} messages.'))
    print(sub('Your favorite color is {color}'))


if __name__ == '__main__':
    var_str()

