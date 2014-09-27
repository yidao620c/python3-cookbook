#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
Topic: 序列化一个对象
Desc : 
"""
import pickle


def serailize_object():
    data = [1, 2, 3]
    f = open('somefile', 'wb')
    pickle.dump(data, f)

    # 将对象转储为字符串
    s = pickle.dumps(data)

    # Restore from a file
    f = open('somefile', 'rb')
    data = pickle.load(f)

    # Restore from a string
    data = pickle.loads(s)

    f = open('somedata', 'wb')
    pickle.dump([1, 2, 3, 4], f)
    pickle.dump('hello', f)
    pickle.dump({'Apple', 'Pear', 'Banana'}, f)
    f.close()

    f = open('somedata', 'rb')
    print(pickle.load(f))
    print(pickle.load(f))
    print(pickle.load(f))

if __name__ == '__main__':
    serailize_object()
