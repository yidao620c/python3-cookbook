#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
Topic: 使用yield和send的典型场景
Desc :
get_primes的后几行需要着重解释。yield关键字返回number的值，而像 other = yield foo 这样的语句的意思是，
"返回foo的值，这个值返回给调用者的同时，将other的值也设置为那个值"。
你可以通过send方法来将一个值”发送“给生成器，这时候就是将other值设置为发送的值了。
def get_primes(number):
    while True:
        if is_prime(number):
            number = yield number
        number += 1
通过这种方式，我们可以在每次执行yield的时候为number设置不同的值。
现在我们可以补齐print_successive_primes中缺少的那部分代码：
def print_successive_primes(iterations, base=10):
    prime_generator = get_primes(base)
    prime_generator.send(None)
    for power in range(iterations):
        print(prime_generator.send(base ** power))
这里有两点需要注意：
首先，我们打印的是generator.send的结果，这是没问题的，
因为send在发送数据给生成器的同时还返回生成器通过yield生成的值（就如同生成器中yield语句做的那样）。
第二点，看一下prime_generator.send(None)这一行，
当你用send来“启动”一个生成器时（就是从生成器函数的第一行代码执行到第一个yield语句的位置），
你必须发送None。这不难理解，根据刚才的描述，生成器还没有走到第一个yield语句，
如果我们发送一个真实的值，这时是没有人去“接收”它的。一旦生成器启动了，我们就可以像上面那样发送数据了。
"""
import random


def get_data():
    """返回0到9之间的3个随机数"""
    return random.sample(range(10), 3)


def consume():
    """显示每次传入的整数列表的动态平均值"""
    running_sum = 0
    data_items_seen = 0

    while True:
        print('before 1 yield....')
        data = yield [0, 0, 0]
        print('-------yield inner------- {}'.format(data))
        print('after 1 yield...')
        data_items_seen += len(data)
        running_sum += sum(data)
        print('The running average is {} - {} - {}'.format(
            data_items_seen, running_sum, running_sum / float(data_items_seen)))


def produce(consumer):
    """产生序列集合，传递给消费函数（consumer）"""
    while True:
        data = get_data()
        print('Produced {}'.format(data))
        consumer.send(data)
        yield


if __name__ == '__main__':
    consumer = consume()
    aa = consumer.send(None)
    print(aa)
    bb = consumer.send(get_data())
    print(bb)
    producer = produce(consumer)
    # for _ in range(2):
    #     print('Producing...')
    #     next(producer)
