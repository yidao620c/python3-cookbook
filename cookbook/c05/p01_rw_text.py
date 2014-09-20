#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
Topic: 读写文本文件
Desc : 
"""

def rw_text():
    # Iterate over the lines of the file
    with open('somefile.txt', 'rt') as f:
        for line in f:
            # process line
            print(line)

    # Write chunks of text data
    with open('somefile.txt', 'wt') as f:
        f.write('text1')
        f.write('text2')

if __name__ == '__main__':
    rw_text()

