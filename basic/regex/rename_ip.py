#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
    Topic: sample
    Desc : 重命名io文件名
"""
import sys
import os
import os.path as p
import re
from basic.regex.replace_ip import ip_maps

__author__ = 'Xiong Neng'


def rename_file(path):
    files = os.listdir(path)
    for eachname in files:
        print(eachname)
        for k, v in ip_maps.items():
            if re.search(k + r'(?=\D+|\n|$)', eachname):
                new_name = re.sub(k + r'(?=\D+|\n|$)', v, eachname)
                os.rename(p.join(path, eachname), p.join(path, new_name))
                break


if __name__ == '__main__':
    rename_file(sys.argv[1])
