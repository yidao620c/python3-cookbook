#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
    Topic: sample
    Desc : 
"""
import ch21_unittest.splitter as split
import unittest

__author__ = 'Xiong Neng'


class TestSplit(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_simple_string(self):
        r = split.split("GOOG 100 490.50")
        self.assertEqual(r, ["GOOG", "100", "490.50"])

    def test_type_convert(self):
        r = split.split("GOOG 100 490.50", [str, int, float])
        self.assertEqual(r, ["GOOG", 100, 490.5])

    def test_delimeter(self):
        r = split.split("GOOG,100,490.50", delimiter=",")
        self.assertEqual(r, ["GOOG", "100", "490.50"])


def main():
    split._private_method()  # 模块的protected方法一一个_开头
    unittest.main()


if __name__ == '__main__':
    main()
