#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
Topic: 串行端口数据交换
Desc : 
"""
import serial


def serial_posts():
    ser = serial.Serial('/dev/tty.usbmodem641',  # Device name varies
                        baudrate=9600,
                        bytesize=8,
                        parity='N',
                        stopbits=1)


if __name__ == '__main__':
    serial_posts()

