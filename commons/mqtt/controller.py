#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
Topic: 模拟控制客户端
Desc : 
"""
import paho.mqtt.client as mqtt


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


if __name__ == '__main__':
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message

    client.connect("192.168.203.95", 1883, 60)

    # Blocking call that processes network traffic, dispatches callbacks and
    # handles reconnecting.
    # Other loop*() functions are available that give a threaded interface and a
    # manual interface.
    client.loop_forever()
