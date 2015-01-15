#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
    Topic: sample
    Desc : 服务器套接字

    模板：
    ss = socket()               # 创建服务器套接字
    ss.bind()                   # 把地址绑定到套接字上
    ss.listen()                 # 监听连接
    inf_loop:                   # 服务器无限循环
        cs = ss.accept()        # 接收到客户端套接字
        comm_loop:              # 通信循环
            cs.recv()/cs.send() # 对话(接受与发送)
        cs.close()              # 关闭客户端套接字

    ....
    ss.close()                  # 关闭服务器套接字

"""
from socket import *
from time import ctime
__author__ = 'Xiong Neng'

HOST = ''
PORT = 21567
BUFSIZ = 1024
ADDR = (HOST, PORT)

tcpSerSock = socket(AF_INET, SOCK_STREAM)
tcpSerSock.bind(ADDR)
tcpSerSock.listen(5)

while True:
    print('waiting for connection....')
    tcpCliSock, cliAddr = tcpSerSock.accept()
    print('...connected from', cliAddr)

    while True:
        data = tcpCliSock.recv(BUFSIZ)
        if not data:
            break
        tcpCliSock.send('[%s] %s' % (ctime(), data))

    tcpCliSock.close()

tcpSerSock.close()






