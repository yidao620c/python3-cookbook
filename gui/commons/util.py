#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
Topic: 工具集合
Desc : 
"""
import sys
import os


def resource_path(relative_path):
    """获取实际路径"""
    if hasattr(sys, "_MEIPASS"):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


def userhome_file(filename):
    userhome = os.path.expanduser('~')
    return os.path.join(userhome, filename)