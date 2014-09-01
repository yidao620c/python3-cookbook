#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
    Topic: sample
    Desc : 客户端
"""
from socket import *
__author__ = 'Xiong Neng'

HOST = 'localhost'
PORT = 21567
BUFSIZE = 1024
ADDR = (HOST, PORT)

tcpCliSock = socket(AF_INET, SOCK_STREAM)
tcpCliSock.connect(ADDR)

while True:
    data = input('> ')
    if not data:
        break
    tcpCliSock.send(data)
    data = tcpCliSock.recv(BUFSIZE)
    if not data:
        break
    print(data)

tcpCliSock.close()
