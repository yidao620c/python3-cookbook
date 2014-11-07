#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
Topic: 模拟手机客户端
Desc : 
"""
import paho.mqtt.client as mqtt
import time


# The callback for when the client receives a CONNACK response from the server.
def on_connect(cli, userdata, rc):
    # Subscribing in on_connect() means that if we lose the connection and
    print("Connected with result code " + str(rc))
    # reconnect then subscriptions will be renewed.
    cli.publish("clients/command/{}".format('001'), "Open")
    cli.subscribe('clients/result/{}'.format('001'))


# The callback for when a PUBLISH message is received from the server.
def on_message(cli, userdata, msg):
    print(msg.topic + " " + str(msg.payload))
    cli.disconnect()


def start_connnect(ip):
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(ip, 1883, 60)
    client.loop_start()

if __name__ == '__main__':
    while True:
        time.sleep(1)
