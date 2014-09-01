#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
    Topic: 进程池
    Desc : 
"""
import os
import multiprocessing
import hashlib

__author__ = 'Xiong Neng'

BUFSIZE = 8192
POOLSIZE = 2


def compute_digest(filename):
    try:
        f = open(filename, 'rb')
    except IOError:
        return None
    digest = hashlib.sha512()
    while True:
        chunk = f.read(BUFSIZE)
        if not chunk: break
        digest.update(chunk)
    f.close()
    return filename, digest.digest()


def build_digest_map(topdir):
    digest_pool = multiprocessing.Pool(POOLSIZE)
    allfiles = (os.path.join(path, name)
                for path, dirs, files in os.walk(topdir)
                for name in files)
    digest_map = dict(digest_pool.imap_unordered(compute_digest, allfiles, 20))
    digest_pool.close()
    return digest_map

def demo():
    digest_map = build_digest_map(r'D:\work\projects\core-python')
    print(len(digest_map))


if __name__ == '__main__':
    demo()
