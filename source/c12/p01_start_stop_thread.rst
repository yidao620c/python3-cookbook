============================
12.1 启动与停止线程
============================

----------
问题
----------
为了并发的执行代码, 你想要创建和销毁一些线程

----------
解决方案
----------
``threading`` 库可以用来在自己的线程中执行任意可调用的Python对象.
首先, 你要创建一个 ``Thread`` 实例, 提供一个你想要执行的可调用对象作为目标
这里是一个简单的样例.

.. code-block:: python

    # Code to execute in an independent thread
    import time
    def countdown(n):
        while n > 0:
            print('T-minus', n)
            n -= 1
            time.sleep(5)

    # Create and launch a thread
    from threading import Thread
    t = Thread(target=countdown, args=(10,))
    t.start()

当你创建一个thread实例之后, 除非你调用他的 ``start()`` 方法, 不然他不会启动.( ``start()`` 方法将会调用目标函数同时传入你提供的参数)

线程将会在他们自己的系统级别的线程中运行(比如, 一个POSIX线程或者Windows中的线程), 系统级别的线程完全受控于操作系统.
线程启动后独立运行, 直到目标函数return返回.
你可以查询一个线程实例来看看他是否还在运行:

.. code-block:: python

    if t.is_alive():
        print('Still running')
    else:
        print('Completed')

你以可以请求把他和一个线程结合(join), 这个线程将会等待他运行结束:

.. code-block:: python

    t.join()

解释器将会保持运行知道所有的线程终止. 长期运行的线程或者后台的永久运行的任务, 你应该考虑让他们作为守护进程.
举例:

.. code-block:: python

    t = Thread(target=countdown, args=(10,), daemon=True)
    t.start()

守护进程不能被结合(join). 不管怎样, 他们将会在主线程结束时自动销毁.

在这两种操作之外, 对于线程你没有太多的其他可以使用操作.
比如, 这里没有什么操作可以终结一个线程, 向线程发送信号, 调整他们的时序安排, 或者其他高级的操作.
如果你想要这些特性, 你要自己写.

如果你想要能够终结线程, 这个线程必须规划为向一个选取的点轮询退出.
比如, 你可能吧你的线程放在这样的一个class 中:

.. code-block:: python

    class CountdownTask:
        def __init__(self):
            self._running = True

        def terminate(self):
            self._running = False

        def run(self, n):
            while self._running and n > 0:
                print('T-minus', n)
                n -= 1
                time.sleep(5)


    c = CountdownTask()
    t = Thread(target=c.run, args=(10,))
    t.start()
    ...
    c.terminate() # Signal termination
    t.join() # Wait for actual termination (if needed)

轮询线程的退出在一个线程执行的是阻塞的操作比如I/O的时候变得棘手. 举个例子, 一个线程被不确定的I/O操作阻塞, 他可能永远也无法返回, 检查自己是否被结束.
为了正确处理这样的情况, 你需要利用带有超时的循环小心的规划线程.
比如

.. code-block:: python

    class IOTask:
        def terminate(self):
            # sock is a socket
            sock.settimeout(5)   # set timeout period
            while self._running:
                # Perform a blocking I/O operation w/ timeout
                try:
                    data = sock.recv(8192)
                    break
                except socket.timeout:
                    continue
                # Continued processing
                ...
            # Terminated
            return




----------
讨论
----------
由于 全局解释器锁(GIL), Python线程被限制为任何时候只允许一个线程在解释器中运行的执行模型.
正因如此, python线程通常不用作计算能力加强的任务, 这些任务应该使用多CPU的并行来达到目的.
多线程更适合于读写处理和处理阻塞式的并发任务.(比如, 读写等待, 等待数据库返回的结果等等)

有时你看到线程通过继承 ``Thread`` 类来定义.
比如

.. code-block:: python

    from threading import Thread
    class CountdownThread(Thread):
        def __init__(self, n):
            super().__init__()
            self.n = n

        def run(self):
            while self.n > 0:
                print('T-minus', self.n)
                self.n -= 1
                time.sleep(5)

    c = CountdownThread(5)
    c.start()


尽管他能够运行, 但是这段代码使用了与 ``threading`` 库的额外的关系.
换言之, 本来你只能用配置好的线程的结果, 然而这里的技巧展现出了编写不显式依赖 ``threading`` 的代码.
通过将你的代码从这样的依赖中解放出来, 使得你的代码能被其他包含或者不包含多线程的上下文使用.
比如, 你获取能过运行你的代码在另一个分离的进程中, 通过 ``multiprocessing`` 模块使用:

.. code-block:: python

    import multiprocessing
    c = CountdownTask(5)
    p = multiprocessing.Process(target=c.run)
    p.start()
    ...

再次强调, 这只在 ``CountdownTask`` 类被写在真正意义上的并发的方式下才生效(多线程, 多进程等等)

----------
译者注
----------
定义 ``CountdownTask`` 部分的代码中, 原书部分为 ``self.n = 0`` , 译者运行这段代码发现有问题,认为这个地方是笔误,
正确的应该是 ``self.n = n`` .