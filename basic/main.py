#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
    Topic: sample
    Desc : 
"""
import sys, os
from yidao.core import add_subtract
__author__ = 'Xiong Neng'

def test_f(fmt, *args, exc_info, extra):
    print(fmt)
    print(len(args))
    print(exc_info)
    print(extra)
    add_subtract.doprob()

if __name__ == '__main__':
   if -1:
       print("aaa")
