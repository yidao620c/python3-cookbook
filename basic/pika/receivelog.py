#!/usr/bin/env python
import pika

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()
channel.exchange_declare(exchange='logs')
result = channel.queue_declare(queue='logqueue')
queue_name = result.method.queue
# 新建一个queue，并且把它绑定到一个exchange上面，并且指定routing_key
channel.queue_bind(exchange='logs', routing_key='log', queue=queue_name)
print('[*] Waiting for logs. To exit press CTRL+C')


def callback(ch, method, properties, body):
    print("[x] %r" % (body,))

# 这个就是直接消费一个queue了
channel.basic_consume(callback, queue=queue_name, no_ack=True)
channel.start_consuming()