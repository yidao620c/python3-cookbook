#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
Topic: 使用partial函数来减少参数个数
Desc : 
"""
import logging
from multiprocessing import Pool
from functools import partial
from socketserver import StreamRequestHandler, TCPServer


def spam(a, b, c, d):
    print(a, b, c, d)


def output_result(result, log=None):
    if log is not None:
        log.debug('Got: %r', result)


# A sample function
def add(x, y):
    return x + y


class EchoHandler(StreamRequestHandler):
    # ack is added keyword-only argument. *args, **kwargs are
    # any normal parameters supplied (which are passed on)
    def __init__(self, *args, ack, **kwargs):
        self.ack = ack
        super().__init__(*args, **kwargs)

    def handle(self):
        for line in self.rfile:
            self.wfile.write(self.ack + line)

if __name__ == '__main__':
    s1 = partial(spam, 1) # a = 1
    s1(2, 3, 4)
    s1(4, 5, 6)
    s2 = partial(spam, d=42) # d = 42
    s2(1, 2, 3)
    s2(4, 5, 5)
    s3 = partial(spam, 1, 2, d=42) # a = 1, b = 2, d = 42
    s3(3)
    s3(4)

    logging.basicConfig(level=logging.DEBUG)
    log = logging.getLogger('test')

    p = Pool()
    p.apply_async(add, (3, 4), callback=partial(output_result, log=log))
    p.close()
    p.join()

    # socket服务器
    serv = TCPServer(('', 15000), partial(EchoHandler, ack=b'RECEIVED:'))
    serv.serve_forever()

