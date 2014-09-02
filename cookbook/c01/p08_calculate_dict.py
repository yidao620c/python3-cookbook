#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
Topic: 字典的数据运算
Desc : 
"""


def calc_dict():
    prices = {
        'ACME': 45.23,
        'AAPL': 612.78,
        'IBM': 205.55,
        'HPQ': 37.20,
        'FB': 10.75
    }

    min_price = min(zip(prices.values(), prices.keys()))
    # min_price is (10.75, 'FB')
    max_price = max(zip(prices.values(), prices.keys()))
    # max_price is (612.78, 'AAPL')

    prices_sorted = sorted(zip(prices.values(), prices.keys()))
    # prices_sorted is [(10.75, 'FB'), (37.2, 'HPQ'),
    #                   (45.23, 'ACME'), (205.55, 'IBM'),
    #                   (612.78, 'AAPL')]

    prices_and_names = zip(prices.values(), prices.keys())
    print(min(prices_and_names)) # OK
    print(max(prices_and_names)) # ValueError: max() arg is an empty sequence

    min(prices) # Returns 'AAPL'
    max(prices) # Returns 'IBM'

    min(prices, key=lambda k: prices[k]) # Returns 'FB'
    max(prices, key=lambda k: prices[k]) # Returns 'AAPL'

    min_value = prices[min(prices, key=lambda k: prices[k])]

    prices = { 'AAA' : 45.23, 'ZZZ': 45.23 }
    min(zip(prices.values(), prices.keys()))
    # (45.23, 'AAA')
    max(zip(prices.values(), prices.keys()))
    # (45.23, 'ZZZ')
