#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
Topic: 模拟家电
Desc : 
"""
import paho.mqtt.client as mqtt


# The callback for when the client receives a CONNACK response from the server.
def on_connect(cli, userdata, rc):
    # Subscribing in on_connect() means that if we lose the connection and
    print("Connected with result code " + str(rc))
    # reconnect then subscriptions will be renewed.
    cli.subscribe("clients/command/+")


def on_connect2(cli, userdata, rc):
    # Subscribing in on_connect() means that if we lose the connection and
    print("Connected with result code " + str(rc))
    # reconnect then subscriptions will be renewed.
    cli.publish("clients/result/{}".format('001'), "Success")
    cli.disconnect()


# The callback for when a PUBLISH message is received from the server.
def on_message(cli, userdata, msg):
    print(msg.topic + " " + str(msg.payload))
    cli.publish("clients/result/{}".format('001'), "Success")
    client2 = mqtt.Client()
    client2.on_connect = on_connect2
    client2.connect("192.168.203.107", 1883, 60)
    client2.loop_forever()


if __name__ == '__main__':
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message

    client.connect("192.168.203.107", 1883, 60)

    # Blocking call that processes network traffic, dispatches callbacks and
    # handles reconnecting.
    # Other loop*() functions are available that give a threaded interface and a
    # manual interface.
    client.loop_forever()
