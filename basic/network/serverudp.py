#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
    Topic: sample
    Desc : 服务器套接字UDP
"""
from socket import *
from time import ctime
__author__ = 'Xiong Neng'

HOST = ''
PORT = 21567
BUFSIZ = 1024
ADDR = (HOST, PORT)

udpSerSock = socket(AF_INET, SOCK_DGRAM)
udpSerSock.bind(ADDR)

while True:
    print('waiting for udp messages....')
    data, cliAddr = udpSerSock.recvfrom(BUFSIZ)
    print('...connected from', cliAddr)

    udpSerSock.sendto('[%s] %s' % (ctime(), data), cliAddr)
    print('have received from and returned to : ', cliAddr)

udpSerSock.close()






