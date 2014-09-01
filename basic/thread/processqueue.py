#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
    Topic: 多进程通信，使用消息队列通信
    Desc : 
"""
import multiprocessing
import time

__author__ = 'Xiong Neng'


def consumer(input_q):
    while True:
        item = input_q.get()
        print(item)
        input_q.task_done()


def producer(seq, output_q):
    for item in seq:
        output_q.put(item)
        time.sleep(0.6)


def demo():
    q = multiprocessing.JoinableQueue()  # 可连接的共享进程队列
    cons_p = multiprocessing.Process(target=consumer, args=(q, ))
    cons_p.daemon = True
    cons_p.start()

    seq = [1, 2, 3, 4, 5]
    producer(seq, q)

    q.join()  # 保证在主进程退出前，共享队列中所有元素都被处理完了


if __name__ == '__main__':
    demo()
