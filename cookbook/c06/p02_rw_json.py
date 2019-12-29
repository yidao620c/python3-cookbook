#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
Topic: JSON读写
Desc :
"""
import json
from collections import OrderedDict


class JSONObject:
    def __init__(self, d):
        self.__dict__ = d


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y


def serialize_instance(obj):
    d = {'__classname__': type(obj).__name__}
    d.update(vars(obj))
    return d


def unserialize_object(d):
    clsname = d.pop('__classname__', None)
    if clsname:
        cls = classes[clsname]
        obj = cls.__new__(cls)  # Make instance without calling __init__
        for key, value in d.items():
            setattr(obj, key, value)
            return obj
    else:
        return d

# Dictionary mapping names to known classes
classes = {
    'Point': Point
}


def rw_json():
    data = {
        'name': 'ACME',
        'shares': 100,
        'price': 542.23
    }

    json_str = json.dumps(data)  # str类型
    data = json.loads(json_str)

    # Writing JSON data
    with open('data.json', 'w') as f:
        json.dump(data, f)

    # Reading data back
    with open('data.json', 'r') as f:
        data = json.load(f)

    # 使用object_pairs_hook
    s = '{"name": "ACME", "shares": 50, "price": 490.1}'
    data = json.loads(s, object_pairs_hook=OrderedDict)
    print(data)

    # 解码为自定义对象
    # data = json.loads(s, object_hook=JSONObject)
    # print(data.name)
    # print(data.shares)

    print(json.dumps(data))
    print(json.dumps(data, indent=4))

    p = Point(2, 3)
    s = json.dumps(p, default=serialize_instance)
    print(s)
    a = json.loads(s, object_hook=unserialize_object)
    print(a)


if __name__ == '__main__':
    rw_json()

