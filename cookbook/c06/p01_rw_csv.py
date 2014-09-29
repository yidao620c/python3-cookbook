#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
Topic: 读写CSV数据
Desc : 
"""
import csv
from collections import namedtuple


def rw_csv():
    with open('stocks.csv') as f:
        f_csv = csv.reader(f)
        headers = next(f_csv)
        for row in f_csv:
            print(row)

    with open('stocks.csv') as f:
        f_csv = csv.reader(f)
        headings = next(f_csv)
        Row = namedtuple('Row', headings)
        for r in f_csv:
            row = Row(*r)
            # Process row
            print(row.Change)

    headers = ['Symbol', 'Price', 'Date', 'Time', 'Change', 'Volume']
    rows = [('AA', 39.48, '6/11/2007', '9:36am', -0.18, 181800),
            ('AIG', 71.38, '6/11/2007', '9:36am', -0.15, 195500),
            ('AXP', 62.58, '6/11/2007', '9:36am', -0.46, 935000),
    ]

    with open('stocks.csv', 'w') as f:
        f_csv = csv.writer(f)
        f_csv.writerow(headers)
        f_csv.writerows(rows)


if __name__ == '__main__':
    rw_csv()

