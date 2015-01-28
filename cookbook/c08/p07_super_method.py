#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
Topic: sample
Desc : 
"""


class A:
    def spam(self):
        print('A.spam')


class B(A):
    def spam(self):
        print('B.spam')
        super().spam()  # Call parent spam()


class A1:
    def __init__(self):
        self.x = 0


class B1(A1):
    def __init__(self):
        super().__init__()
        self.y = 1


class Proxy():
    def __init__(self, obj):
        self._obj = obj

    # Delegate attribute lookup to internal obj
    def __getattr__(self, name):
        return getattr(self._obj, name)

    # Delegate attribute assignment
    def __setattr__(self, name, value):
        if name.startswith('_'):
            super().__setattr__(name, value)  # Call original __setattr__
        else:
            setattr(self._obj, name, value)


class Base:
    def __init__(self):
        print('Base.__init__')


class AA(Base):
    def __init__(self):
        super().__init__()
        print('AA.__init__')


class BB(Base):
    def __init__(self):
        super().__init__()
        print('BB.__init__')


class CC(AA, BB):
    def __init__(self):
        super().__init__()  # Only one call to super() here
        print('CC.__init__')


CC()
print(CC.__mro__)


class A3:
    def spam(self):
        print('A3.spam')
        super().spam()


class B3:
    def spam(self):
        print('B3.spam')


class C3(A3, B3):
    pass

print(C3.__mro__)
C3().spam()