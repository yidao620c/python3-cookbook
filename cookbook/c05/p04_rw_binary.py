#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
Topic: 读写二进制文件
Desc : 
"""


def rw_binary():
    # Read the entire file as a single byte string
    with open('somefile.bin', 'rb') as f:
        data = f.read()

    # Write binary data to a file
    with open('somefile.bin', 'wb') as f:
        f.write(b'Hello World')

    # Text string
    t = 'Hello World'
    print(t[0])

    # Byte string
    b = b'Hello World'
    print(b[0])
    for c in b:
        print(c)

if __name__ == '__main__':
    rw_binary()

