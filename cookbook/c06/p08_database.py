#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
Topic: 关系型数据库处理
Desc : 
"""
import sqlite3
import datetime.time


def db_operation():
    db = sqlite3.connect('database.db')
    c = db.cursor()
    c.execute('create table portfolio (symbol text, shares integer, price real)')
    db.commit()

    stocks = [
        ('GOOG', 100, 490.1),
        ('AAPL', 50, 545.75),
        ('FB', 150, 7.45),
        ('HPQ', 75, 33.2),
    ]
    c.executemany('insert into portfolio values (?,?,?)', stocks)
    db.commit()

    for row in db.execute('select * from portfolio'):
        print(row)

    min_price = 12
    for row in db.execute('select * from portfolio where price >= ?', (min_price,)):
        print(row)

if __name__ == '__main__':
    db_operation()

