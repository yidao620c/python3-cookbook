#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
    Topic: 进程间使用管道通信
    Desc : 
"""
import multiprocessing
__author__ = 'Xiong Neng'

def consumer(pipe):
    outp, inp = pipe
    inp.close()
    while True:
        try:
            item = outp.recv()
        except EOFError:
            break
        print(item)
    print('comsumer done')

def producer(seq, inp):
    for item in seq:
        inp.send(item)

def demo():
    (outp, inp) = multiprocessing.Pipe()
    consp = multiprocessing.Process(target=consumer, args=((outp, inp), ))
    consp.start()

    outp.close()

    seq = [1, 3, 4, 5]
    producer(seq, inp)

    inp.close()

    consp.join()

if __name__ == '__main__':
    demo()
