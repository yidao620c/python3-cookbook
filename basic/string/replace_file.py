#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
Topic: 查找并替换文本文件
Desc :
"""

import os
import os.path as p
import re


def search_replace():
    """将cookbooksource目录中所有rst的标题加上序号"""
    init_path = r'D:\work\gitproject\python3-cookbook\source'
    for i in range(1, 16):
        each_chapter = '%s\c%s' % (init_path, '%02d' % i)
        files = os.listdir(each_chapter)
        for f in files:
            full_path = p.join(each_chapter, f)
            if p.isfile(full_path):
                with open(full_path, mode='r', encoding='utf-8') as readf:
                    old_lines = readf.readlines()
                old_lines[1] = '%s%s' % ('%d.%d ' % (i, int(f[1:3])), old_lines[1])
                with open(full_path, mode='w', encoding='utf-8') as writef:
                    writef.writelines(old_lines)


if __name__ == '__main__':
    search_replace()