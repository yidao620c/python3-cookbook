==============================
13.6 执行外部命令并获取它的输出
==============================

----------
问题
----------
You want to execute an external command and collect its output as a Python string.

|

----------
解决方案
----------
Use the subprocess.check_output() function. For example:

import subprocess
out_bytes = subprocess.check_output(['netstat','-a'])

This runs the specified command and returns its output as a byte string. If you need to
interpret the resulting bytes as text, add a further decoding step. For example:

out_text = out_bytes.decode('utf-8')

If the executed command returns a nonzero exit code, an exception is raised. Here is
an example of catching errors and getting the output created along with the exit code:

try:
    out_bytes = subprocess.check_output(['cmd','arg1','arg2'])
except subprocess.CalledProcessError as e:
    out_bytes = e.output       # Output generated before error
    code      = e.returncode   # Return code

By default, check_output() only returns output written to standard output. If you want
both standard output and error collected, use the stderr argument:

out_bytes = subprocess.check_output(['cmd','arg1','arg2'],
                                    stderr=subprocess.STDOUT)

If you need to execute a command with a timeout, use the timeout argument:

try:
    out_bytes = subprocess.check_output(['cmd','arg1','arg2'], timeout=5)
except subprocess.TimeoutExpired as e:
    ...

Normally, commands are executed without the assistance of an underlying shell (e.g.,
sh, bash, etc.). Instead, the list of strings supplied are given to a low-level system com‐
mand, such as os.execve(). If you want the command to be interpreted by a shell,
supply it using a simple string and give the shell=True argument. This is sometimes
useful if you’re trying to get Python to execute a complicated shell command involving
pipes, I/O redirection, and other features. For example:

out_bytes = subprocess.check_output('grep python | wc > out', shell=True)

Be aware that executing commands under the shell is a potential security risk if argu‐
ments are derived from user input. The shlex.quote() function can be used to properly
quote arguments for inclusion in shell commands in this case.

|

----------
讨论
----------
The check_output() function is the easiest way to execute an external command and
get its output. However, if you need to perform more advanced communication with a

subprocess, such as sending it input, you’ll need to take a difference approach. For that,
use the subprocess.Popen class directly. For example:

import subprocess

# Some text to send
text = b'''
hello world
this is a test
goodbye
'''

# Launch a command with pipes
p = subprocess.Popen(['wc'],
          stdout = subprocess.PIPE,
          stdin = subprocess.PIPE)

# Send the data and get the output
stdout, stderr = p.communicate(text)

# To interpret as text, decode
out = stdout.decode('utf-8')
err = stderr.decode('utf-8')

The subprocess module is not suitable for communicating with external commands
that expect to interact with a proper TTY. For example, you can’t use it to automate tasks
that ask the user to enter a password (e.g., a ssh session). For that, you would need to
turn to a third-party module, such as those based on the popular “expect” family of tools
(e.g., pexpect or similar).
