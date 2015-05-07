============================
12.14 在Unix系统上面启动守护进程
============================

----------
问题
----------
You would like to write a program that runs as a proper daemon process on Unix or
Unix-like systems.

Solution
Creating a proper daemon process requires a precise sequence of system calls and careful
attention to detail. The following code shows how to define a daemon process along
with the ability to easily stop it once launched:

#!/usr/bin/env python3
# daemon.py

import os
import sys

import atexit
import signal

def daemonize(pidfile, *, stdin='/dev/null',
                          stdout='/dev/null',
                          stderr='/dev/null'):

    if os.path.exists(pidfile):
        raise RuntimeError('Already running')

    # First fork (detaches from parent)
    try:
        if os.fork() > 0:
            raise SystemExit(0)   # Parent exit
    except OSError as e:
        raise RuntimeError('fork #1 failed.')

    os.chdir('/')
    os.umask(0)
    os.setsid()
    # Second fork (relinquish session leadership)
    try:
        if os.fork() > 0:
            raise SystemExit(0)
    except OSError as e:
        raise RuntimeError('fork #2 failed.')

    # Flush I/O buffers
    sys.stdout.flush()
    sys.stderr.flush()

    # Replace file descriptors for stdin, stdout, and stderr
    with open(stdin, 'rb', 0) as f:
        os.dup2(f.fileno(), sys.stdin.fileno())
    with open(stdout, 'ab', 0) as f:
        os.dup2(f.fileno(), sys.stdout.fileno())
    with open(stderr, 'ab', 0) as f:
        os.dup2(f.fileno(), sys.stderr.fileno())

    # Write the PID file
    with open(pidfile,'w') as f:
        print(os.getpid(),file=f)

    # Arrange to have the PID file removed on exit/signal
    atexit.register(lambda: os.remove(pidfile))

    # Signal handler for termination (required)
    def sigterm_handler(signo, frame):
        raise SystemExit(1)

    signal.signal(signal.SIGTERM, sigterm_handler)

def main():
    import time
    sys.stdout.write('Daemon started with pid {}\n'.format(os.getpid()))
    while True:
        sys.stdout.write('Daemon Alive! {}\n'.format(time.ctime()))
        time.sleep(10)

if __name__ == '__main__':
    PIDFILE = '/tmp/daemon.pid'

    if len(sys.argv) != 2:
        print('Usage: {} [start|stop]'.format(sys.argv[0]), file=sys.stderr)
        raise SystemExit(1)

    if sys.argv[1] == 'start':
        try:
            daemonize(PIDFILE,
                      stdout='/tmp/daemon.log',
                      stderr='/tmp/dameon.log')
        except RuntimeError as e:
            print(e, file=sys.stderr)
            raise SystemExit(1)

        main()

    elif sys.argv[1] == 'stop':
        if os.path.exists(PIDFILE):
            with open(PIDFILE) as f:
                os.kill(int(f.read()), signal.SIGTERM)
        else:
            print('Not running', file=sys.stderr)
            raise SystemExit(1)

    else:
        print('Unknown command {!r}'.format(sys.argv[1]), file=sys.stderr)
        raise SystemExit(1)

To launch the daemon, the user would use a command like this:

bash % daemon.py start
bash % cat /tmp/daemon.pid
2882
bash % tail -f /tmp/daemon.log
Daemon started with pid 2882
Daemon Alive! Fri Oct 12 13:45:37 2012
Daemon Alive! Fri Oct 12 13:45:47 2012
...

Daemon processes run entirely in the background, so the command returns immedi‐
ately. However, you can view its associated pid file and log, as just shown. To stop the
daemon, use:

bash % daemon.py stop
bash %

Discussion
This recipe defines a function daemonize() that should be called at program startup to
make the program run as a daemon. The signature to daemonize() is using keyword-
only arguments to make the purpose of the optional arguments more clear when used.
This forces the user to use a call such as this:

daemonize('daemon.pid',
          stdin='/dev/null,
          stdout='/tmp/daemon.log',
          stderr='/tmp/daemon.log')

As opposed to a more cryptic call such as:
# Illegal. Must use keyword arguments
daemonize('daemon.pid',
          '/dev/null', '/tmp/daemon.log','/tmp/daemon.log')

The steps involved in creating a daemon are fairly cryptic, but the general idea is as
follows. First, a daemon has to detach itself from its parent process. This is the purpose
of the first os.fork() operation and immediate termination by the parent.
After the child has been orphaned, the call to  os.setsid() creates an entirely new
process session and sets the child as the leader. This also sets the child as the leader of
a new process group and makes sure there is no controlling terminal. If this all sounds
a bit too magical, it has to do with getting the daemon to detach properly from the
terminal and making sure that things like signals don’t interfere with its operation.
The calls to os.chdir() and os.umask(0) change the current working directory and
reset the file mode mask. Changing the directory is usually a good idea so that the
daemon is no longer working in the directory from which it was launched.
The second call to os.fork() is by far the more mysterious operation here. This step
makes the daemon process give up the ability to acquire a new controlling terminal and
provides even more isolation (essentially, the daemon gives up its session leadership
and thus no longer has the permission to open controlling terminals). Although you
could probably omit this step, it’s typically recommended.
Once the daemon process has been properly detached, it performs steps to reinitialize
the standard I/O streams to point at files specified by the user. This part is actually
somewhat tricky. References to file objects associated with the standard I/O streams are
found in multiple places in the interpreter (sys.stdout, sys.__stdout__, etc.). Simply
closing sys.stdout and reassigning it is not likely to work correctly, because there’s no
way to know if it will fix all uses of sys.stdout. Instead, a separate file object is opened,
and the os.dup2() call is used to have it replace the file descriptor currently being used

by sys.stdout. When this happens, the original file for sys.stdout will be closed and
the new one takes its place. It must be emphasized that any file encoding or text handling
already applied to the standard I/O streams will remain in place.
A common practice with daemon processes is to write the process ID of the daemon in
a file for later use by other programs. The last part of the daemonize() function writes
this file, but also arranges to have the file removed on program termination. The atex
it.register() function registers a function to execute when the Python interpreter
terminates. The definition of a signal handler for SIGTERM is also required for a graceful
termination. The signal handler merely raises SystemExit() and nothing more. This
might look unnecessary, but without it, termination signals kill the interpreter without
performing the cleanup actions registered with  atexit.register(). An example of
code that kills the daemon can be found in the handling of the stop command at the
end of the program.
More information about writing daemon processes can be found in Advanced Pro‐
gramming in the UNIX Environment, 2nd Edition, by W. Richard Stevens and Stephen
A. Rago (Addison-Wesley, 2005). Although focused on C programming, all of the ma‐
terial is easily adapted to Python, since all of the required POSIX functions are available
in the standard library.

