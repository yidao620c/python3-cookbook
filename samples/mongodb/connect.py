#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
Topic: pymongo模块
Desc : 
"""
from pymongo import Connection

if __name__ == '__main__':
    connection = Connection('localhost', 27017)
    db = connection.prefs
    collection = db.location
    for doc in collection.find():
        print(doc)
    connection.close()
