#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
Topic: 控制导入内容
Desc : 
"""

# somemodule.py
def spam():
    pass


def grok():
    pass


blah = 42
# Only export 'spam' and 'grok'
__all__ = ['spam', 'grok']

