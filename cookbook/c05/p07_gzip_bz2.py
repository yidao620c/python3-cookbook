#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
Topic: 读写压缩文件
Desc : 
"""
import gzip
import bz2


def gzip_bz2():
    with gzip.open('somefile.gz', 'rt') as f:
        text = f.read()
    with bz2.open('somefile.bz2', 'rt') as f:
        text = f.read()

    with gzip.open('somefile.gz', 'wt') as f:
        f.write(text)
    with bz2.open('somefile.bz2', 'wt') as f:
        f.write(text)
    with gzip.open('somefile.gz', 'wt', compresslevel=5) as f:
        f.write(text)

    # 作用在已打开的二进制文件上
    f = open('somefile.gz', 'rb')
    with gzip.open(f, 'rt') as g:
        text = g.read()

if __name__ == '__main__':
    gzip_bz2()
