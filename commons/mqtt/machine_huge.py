#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
Topic: 模拟家电
Desc : 
"""
import paho.mqtt.client as mqtt
import gevent
import time


# The callback for when the client receives a CONNACK response from the server.
def on_connect(cli, userdata, rc):
    # Subscribing in on_connect() means that if we lose the connection and
    print("Connected with result code " + str(rc))
    # reconnect then subscriptions will be renewed.
    cli.subscribe("clients/command/+")


def on_connect2(cli, userdata, rc):
    print("Connected with result code " + str(rc))
    cli.publish("clients/result/{}".format('001'), "Success")
    cli.disconnect()


# The callback for when a PUBLISH message is received from the server.
def on_message(cli, userdata, msg):
    print(msg.topic + " " + str(msg.payload))
    cli.publish("clients/result/{}".format('001'), "Success")
    client2 = mqtt.Client()
    client2.on_connect = on_connect2
    client2.connect("192.168.203.107", 1883, 60)
    client2.loop_start()


def start_connnect(ip):
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(ip, 1883, 60)
    client.loop_start()

if __name__ == '__main__':
    threads = [gevent.spawn(start_connnect, '192.168.203.107') for i in range(500)]
    gevent.joinall(threads)
    while True:
        time.sleep(1)
