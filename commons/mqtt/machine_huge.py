#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
Topic: 模拟家电
Desc : 
"""
import paho.mqtt.client as mqtt
import time
import threading


# The callback for when the client receives a CONNACK response from the server.
def on_connect(cli, userdata, rc):
    # Subscribing in on_connect() means that if we lose the connection and
    print("Connected with result code " + str(rc))
    # reconnect then subscriptions will be renewed.
    cli.subscribe("clients/command/+")


# The callback for when a PUBLISH message is received from the server.
def on_message(cli, userdata, msg):
    print(msg.topic + " " + str(msg.payload))


def start_connect_repeat(ip, count):
    for i in range(count):
        start_connect(ip)


def start_connect(ip):
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(ip, 1883, 60)
    client.loop_start()

if __name__ == '__main__':
    for i in range(8000):
        start_connect('192.168.203.107')
    while True:
        time.sleep(1)
