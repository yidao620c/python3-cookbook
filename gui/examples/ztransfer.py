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
import os
import zipfile
import logging

HOSTNAME = '115.29.145.245'  # remote hostname where SSH server is running
PORT = 22
USERNAME = 'winhong'
PASSWORD = 'jianji2014'
# RSA_PRIVATE_KEY = r"/home/paramikouser/.ssh/rsa_private_key"

DIR_LOCAL = r'D:\Wingarden\src\trunk\ling\target\classes\com'
DIR_REMOTE = r"/usr/local/apache-tomcat-8.0.15/webapps/ROOT/WEB-INF/classes/com"
COMMAND_01 = '/home/winhong/ling01.sh'
COMMAND_02 = '/home/winhong/ling02.sh'

ZIPDIR_SRC = r'D:\Wingarden\src\trunk\ling\target\classes\com'
ZIPDIR_DEST = r'D:\Wingarden\src\trunk\ling'
ZIPNAME = 'ling.zip'

# get host key, if we know one
# HOSTKEYTYPE = None
# HOSTKEY = None

logging.basicConfig(level=logging.INFO)
LOG = logging.getLogger('test')


def zipdir(path, zipf):
    for root, dirs, files in os.walk(path):
        for file in files:
            zipf.write(os.path.join(root, file), os.path.join(root.split('\com\\', 1)[1],file))


def ziputil(zip_dir_src, zip_dir_dest, zip_name):
    zipf = zipfile.ZipFile(os.path.join(zip_dir_dest, zip_name), 'w', zipfile.ZIP_DEFLATED)
    zipdir(zip_dir_src, zipf)
    zipf.close()
    return zip_dir_dest, zip_name


def transfer_file(hostname_, port_, username_, password_, fdir_, fname_):
    try:
        print('Establishing SSH connection to:', hostname_, port_, '...')
        t = paramiko.Transport((hostname_, port_))
        t.start_client()

        if not t.is_authenticated():
            print('Trying password login...')
            t.auth_password(username=username_, password=password_)

        sftp = paramiko.SFTPClient.from_transport(t)

        local_file = os.path.join(fdir_, fname_)
        remote_file = DIR_REMOTE + '/' + fname_
        try:
            print('start transport...')
            sftp.put(local_file, remote_file)
        except:
            LOG.error('error...')
            raise
        t.close()
        LOG.info('传输完成后删除本地的zip文件...')
        os.remove(local_file)
    except Exception as e:
        print(e)
        try:
            LOG.info('end transport and close it...')
            t.close()
        except:
            pass


def exe_command(hostname_, username_, password_, commandpaths_):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname_, username=username_, password=password_)
    # channel = ssh.invoke_shell()
    # ssh_stdin, ssh_stdout, ssh_stderr = channel.exec_command(commandpath_)
    for command_ in commandpaths_:
        commandpath_, issudo = command_
        ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command(commandpath_, get_pty=issudo)
        for eline in ssh_stdout.readlines():
            print 'ssh_stdout:%s' % (eline,), ''
        for eline in ssh_stderr.readlines():
            print 'ssh_stderr:%s' % (eline,), ''
        # Cleanup
        ssh_stdin.close()
        ssh_stdout.close()
        ssh_stderr.close()
    # channel.close()
    ssh.close()
    LOG.info('end successfully!')
    return True


def main():
    # 第一步：zip压缩包
    ffdir, ffname = ziputil(ZIPDIR_SRC, ZIPDIR_DEST, ZIPNAME)
    # 第二步：SSH传输压缩包
    transfer_file(HOSTNAME, PORT, USERNAME, PASSWORD, ffdir, ffname)
    # 第三步：执行远程shell脚本，替换class文件并重启，注意sudo和非sudo分开执行
    return exe_command(HOSTNAME, USERNAME, PASSWORD, [(COMMAND_01, True), (COMMAND_02, False)])


if __name__ == '__main__':
    main()

