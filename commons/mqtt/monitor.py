#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
Topic: MQTT消息服务器系统监控
"""
import paho.mqtt.client as mqtt
import gevent
import random
import time


# The callback for when the client receives a CONNACK response from the server.
def on_connect(cli, userdata, rc):
    # Subscribing in on_connect() means that if we lose the connection and
    print(userdata + ":" + "Connected " + str(rc))
    # broker当前连接状态的客户端数量
    cli.subscribe("$SYS/broker/clients/active")


# The callback for when a PUBLISH message is received from the server.
def on_message(cli, userdata, msg):
    print(userdata + ":" + msg.topic + " " + str(msg.payload))


def mqtt_connect(ip):
    c = mqtt.Client(userdata=ip)
    c.on_connect = on_connect
    c.on_message = on_message
    c.connect(ip, 1883, 60)
    c.loop_start()


if __name__ == '__main__':
    threads = [gevent.spawn(mqtt_connect, i)
               for i in ['192.168.203.95', '192.168.203.93', '192.168.203.94']]
    gevent.joinall(threads)
    while True:
        time.sleep(1)

