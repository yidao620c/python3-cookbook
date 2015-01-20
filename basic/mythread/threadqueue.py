#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
    Topic: 使用队列的线程示例
    Desc : 
"""
import threading
from queue import Queue

__author__ = 'Xiong Neng'


class WorkerThread(threading.Thread):
    def __init__(self, *args, **kwargs):
        threading.Thread.__init__(self, *args, **kwargs)
        self.inputq = Queue()

    def send(self, item):
        self.inputq.put(item)


    def close(self):
        self.inputq.put(None)
        self.inputq.join()


    def run(self):
        while True:
            item = self.inputq.get()
            if not item:
                break
            print(item, end=',')
            self.inputq.task_done()
        self.inputq.task_done()
        return


def demo():
    w = WorkerThread()
    w.start()
    w.send('hello test ')
    w.send('world')
    w.close()


if __name__ == '__main__':
    demo()
