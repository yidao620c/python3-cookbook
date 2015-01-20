#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
Topic: paramiko模块演示
https://github.com/paramiko/paramiko/tree/master/demos

安装python3-pycrypto-windows
python3.4版本之前：http://www.voidspace.org.uk/python/modules.shtml#pycrypto
python3.4最新版本：https://github.com/axper/python3-pycrypto-windows-installer

先安装Visual C++ 2010 Express，这个是免费的：
http://www.visualstudio.com/zh-cn/downloads/download-visual-studio-vs#DownloadFamilies_4

安装后可以先试着pip install paramiko看能不能成功，如果还不行就再下载下面的：
如果安装上面的最后提示还有个SQL Server 2008 Express Service Pack1没安装成功，那么自己手动去下载安装：
http://www.microsoft.com/zh-tw/download/details.aspx?id=25052

pip install paramiko
"""
import paramiko

if __name__ == '__main__':
    server = '192.168.203.95'
    username = 'root'
    password = 'root'
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(server, username=username, password=password)
    # channel = ssh.invoke_shell()
    ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command('/home/mango/work/update.sh')
    for eline in ssh_stdout.readlines():
        print('ssh_stdout:{}'.format(eline), end='')
    for eline in ssh_stderr.readlines():
        print('ssh_stderr:{}'.format(eline), end='')
    # Cleanup
    ssh_stdin.close()
    ssh_stdout.close()
    ssh_stderr.close()

    # channel.close()
    ssh.close()

