#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
Topic: 利用MySQL Connector/Python 操作mysql数据库

网址：http://dev.mysql.com/doc/connector-python/en/index.html

"""
import mysql.connector
from mysql.connector import errorcode


def _connect():
    config = {
        'user': 'root',
        'password': 'mysql',
        'host': '192.168.203.95',
        'database': 'hangxin',
        'raise_on_warnings': True,
    }
    cnx = None
    try:
        cnx = mysql.connector.connect(**config)
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)
        if cnx:
            cnx.close()
    return cnx


def _insert():
    pass



