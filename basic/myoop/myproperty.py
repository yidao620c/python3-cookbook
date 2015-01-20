#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
    Topic: 特性property
    Desc : 
"""

__author__ = 'Xiong Neng'


class Foo():
    def __init__(self, name):
        self.__name = name

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, value):
        if not isinstance(value, str):
            raise TypeError("Must be a string.")
        self.__name = value

    @name.deleter
    def name(self):
        raise TypeError("cannot delete name")


def main():
    f = Foo("Guido")
    print(f.name)
    f.name = "Monty"
    print(f.name)
    pass


if __name__ == '__main__':
    main()
