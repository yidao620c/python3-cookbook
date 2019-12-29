#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
Topic: 读写二进制数组结构的数据
Desc : 
"""
from struct import Struct
from collections import namedtuple


def write_records(records, format, f):
    """
    Write a sequence of tuples to a binary file of structures.
    """
    record_struct = Struct(format)
    for r in records:
        f.write(record_struct.pack(*r))


def read_records(format, f):
        record_struct = Struct(format)
        chunks = iter(lambda: f.read(record_struct.size), b'')
        return (record_struct.unpack(chunk) for chunk in chunks)


def unpack_records(format, data):
        record_struct = Struct(format)
        return (record_struct.unpack_from(data, offset)
                for offset in range(0, len(data), record_struct.size))


if __name__ == '__main__':
    records = [(1, 2.3, 4.5),
               (6, 7.8, 9.0),
               (12, 13.4, 56.7)]
    with open('data.b', 'wb') as f:
        write_records(records, '<idd', f)

    # 增量式读取
    with open('data.b','rb') as f:
        for rec in read_records('<idd', f):
            # Process rec
            pass

    # 一次性读取，再分片解析
    with open('data.b', 'rb') as f:
        data = f.read()
    for rec in unpack_records('<idd', data):
        # Process rec
        pass

    record_struct = Struct('<idd')
    # 打印结构的字节数
    print(record_struct.size)
    # 打包数据
    a = record_struct.pack(1, 2.0, 3.0)
    print(a)
    # 解包数据
    print(record_struct.unpack(a))

    # 解包时的命名元组
    Record = namedtuple('Record', ['kind','x','y'])
    with open('data.p', 'rb') as f:
        records = (Record(*r) for r in read_records('<idd', f))
    for r in records:
        print(r.kind, r.x, r.y)

