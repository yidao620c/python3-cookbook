#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
    Topic: sample
    Desc : 将某个文件夹中所有文件放入同名的文件夹中
"""
import sys
import os
import os.path as p

__author__ = 'Xiong Neng'


def move_file_to_dir(path):
    #if len(sys.argv) <= 1:
    #    print('you must specify the path')
    #    exit(1)
    #path = sys.argv[1]
    if not os.path.isdir(path):
        print('wrong path arg... exit')
        exit(1)
    files = os.listdir(path)
    print('current work dir is %s..' % path)
    for eachname in files:
        if p.isfile(p.join(path, eachname)):
            os.mkdir(p.join(path, eachname + "_temp"))
            os.rename(p.join(path, eachname), p.join(path, eachname + '_temp', eachname))
            os.rename(p.join(path, eachname + '_temp'), p.join(path, eachname))


def change_filename(path):
    if not p.isdir(path):
        print('wrong path arg... exit')
        exit(1)
    files = os.listdir(path)
    print('current work dir is %s..' % path)
    count = 1
    for eachname in files:
        fpath = p.join(path, eachname)
        if p.isfile(fpath):
            continue
        fnew = "%03d" % count
        fpathnew = p.join(path, fnew)
        os.rename(fpath, p.join(path, fpathnew))
        count += 1
        eachfiles = os.listdir(fpathnew)
        if len(eachfiles) > 0:
            os.rename(p.join(fpathnew, eachfiles[0]), p.join(fpathnew, fnew + ".JPG"))


def moveout(path):
    if not p.isdir(path):
        print('wrong path arg... exit')
        exit(1)
    files = os.listdir(path)
    print('current work dir is %s..' % path)
    for eachname in files:
        fpath = p.join(path, eachname)
        eachfiles = os.listdir(fpath)
        if len(eachfiles) > 0:
            os.rename(p.join(fpath, eachfiles[0]), p.join(path, eachfiles[0]))


if __name__ == '__main__':
    #change_filename(r"H:\HHHHHHHHHHHHH")
    moveout(r"H:\HHHHHHHHHHHHH")
    pass


