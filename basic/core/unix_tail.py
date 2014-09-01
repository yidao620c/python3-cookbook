#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
    Topic:
        利用generator模仿tail -f www.log | grep "python"
        对变化的日志文件持续查看含有python的行
    Desc : 
"""
import time

__author__ = 'Xiong Neng'


def tail(f):
    f.seek(0, 2)  # 移动到EOF
    while True:
        line = f.readline()
        if not line:
            time.sleep(0.2)
            continue
        yield line


def grep(lines, search_text):
    for line in lines:
        if search_text in line: yield line


def my_tail_search():
    wwwlog = tail(open("www.log"))
    pylines = grep(wwwlog, "python")
    for line in pylines:
        print(line)


def main():
    pass


if __name__ == '__main__':
    main()
