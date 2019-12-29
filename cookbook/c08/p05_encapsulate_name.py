#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
Topic: 隐藏私有属性
Desc : 
"""


class A:
    def __init__(self):
        self._internal = 0  # An internal attribute
        self.public = 1  # A public attribute

    def public_method(self):
        '''
        A public method
        '''
        pass

    def _internal_method(self):
        pass


class B:
    def __init__(self):
        self.__private = 0

    def __private_method(self):
        pass

    def public_method(self):
        pass
        self.__private_method()


class C(B):
    def __init__(self):
        super().__init__()
        self.__private = 1  # Does not override B.__private

    # Does not override B.__private_method()
    def __private_method(self):
        pass