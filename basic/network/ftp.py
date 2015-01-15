#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
    Topic: sample
    Desc : 使用FTP下载示例
"""
import ftplib
import os
import socket
__author__ = 'Xiong Neng'

HOST = 'ftp.mozilla.org'
DIRN = 'pub/webtools'
FILE = 'bugzilla-LATEST.tar.gz'


def main():
    try:
        f = ftplib.FTP(HOST)
    except (socket.error, socket.gaierror) as e:
        print('ERROR: connot reach "%s"' % HOST)
        exit(1)
    print('*** Connected to host "%s"' % HOST)

    try:
        f.login()
    except ftplib.error_perm:
        print('ERROR: connot login anonymously')
        f.quit()
        exit(1)
    print('*** Logged in as "anonymous"')

    try:
        f.cwd(DIRN)
    except ftplib.error_perm:
        print('ERROR: cannot cd to "%s"' % DIRN)
        f.quit()
        exit(1)
    print('*** Changed to "%s" folder' % DIRN)

    try:
        locFile = open(FILE, 'wb')
        f.retrbinary('RETR %s' % FILE, locFile.write)
    except ftplib.error_perm:
        print('ERROR: cannot read file "%s"' % FILE)
        os.unlink(FILE)
    else:
        print('*** Downloaded "%s" to CWD' % FILE)
    finally:
        locFile.close()
    f.quit()
    return

if __name__ == '__main__':
    main()





