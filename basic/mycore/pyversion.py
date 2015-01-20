#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
    Topic: sample
    Desc : 输出python是32位还是64位
"""
import struct

__author__ = 'Xiong Neng'

print(u'%d位' % (struct.calcsize("P") * 8,))
