#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
    Topic: sample
    Desc : 
"""

__author__ = 'Xiong Neng'


def split(line, types=None, delimiter=None):
    """split a line of text and perform type conversion"""
    fields = line.split(delimiter)
    if types:
        fields = [ty(val) for ty, val in zip(types, fields)]
    return fields


def _private_method():
    pass

