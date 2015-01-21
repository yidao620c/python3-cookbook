#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
Topic: 小令自动发布工具
Desc : 
"""
import wx
import examples.ztransfer as ztransfer
import os
import subprocess
import logging
import tempfile
import sys

HOSTNAME_ = '115.29.145.245'  # remote hostname where SSH server is running
USERNAME_ = 'winhong'
PASSWORD_ = 'jianji2014'

_LOGGING = logging.getLogger('zupload')

IS_WIN32 = 'win32' in str(sys.platform).lower()


def subprocess_call(*args, **kwargs):
    # also works for Popen. It creates a new *hidden* window,
    # so it will work in frozen apps (.exe).
    if IS_WIN32:
        _LOGGING.info('subprocess_call==IS_WIN32')
        startupinfo = subprocess.STARTUPINFO()
        startupinfo.dwFlags = subprocess.CREATE_NEW_CONSOLE | subprocess.STARTF_USESHOWWINDOW
        startupinfo.wShowWindow = subprocess.SW_HIDE
        kwargs['startupinfo'] = startupinfo
    retcode = subprocess.call(*args, **kwargs)
    return retcode


def subprocess_popen(*args, **kwargs):
    # also works for Popen. It creates a new *hidden* window,
    # so it will work in frozen apps (.exe).
    if IS_WIN32:
        _LOGGING.info('subprocess_call==IS_WIN32')
        startupinfo = subprocess.STARTUPINFO()
        startupinfo.dwFlags = subprocess.CREATE_NEW_CONSOLE | subprocess.STARTF_USESHOWWINDOW
        startupinfo.wShowWindow = subprocess.SW_HIDE
        kwargs['startupinfo'] = startupinfo
    ppopen = subprocess.Popen(*args, **kwargs)
    return ppopen


class UploadFrame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, -1, u'小令自动发布工具')
        panel = wx.Panel(self)
        # 首先创建controls
        topLbl = wx.StaticText(panel, -1, u'================小令自动发布工具===============')
        topLbl.SetFont(wx.Font(18, wx.SWISS, wx.NORMAL, wx.BOLD))
        nameLbl = wx.StaticText(panel, -1, u'服务器地址:')
        self.name = wx.TextCtrl(panel, -1, HOSTNAME_)  # 文本输入框
        addrLbl = wx.StaticText(panel, -1, u'登录用户名:')
        self.addr1 = wx.TextCtrl(panel, -1, USERNAME_)
        addrLbl2 = wx.StaticText(panel, -1, u'密码:')
        self.addr2 = wx.TextCtrl(panel, -1, PASSWORD_, style=wx.TE_PASSWORD)
        projLbl = wx.StaticText(panel, -1, u'本地工程目录:')
        self.proj = wx.TextCtrl(panel, -1, '')
        mavenbl = wx.StaticText(panel, -1, u'maven目录(选填):')
        self.maven = wx.TextCtrl(panel, -1, '')
        saveBtn = wx.Button(panel, -1, u'开始发布')
        cancelBtn = wx.Button(panel, -1, u'关闭')

        # 下面开始布局
        # mainSizer是顶级sizer，控制所有部件，使用box sizer
        # 垂直sizer
        mainSizer = wx.BoxSizer(wx.VERTICAL)
        # boxsizer.Add(btn1, proportion=0, flag=wx.ALL, border=2)
        mainSizer.Add(topLbl, 0, wx.ALL, 5)
        mainSizer.Add(wx.StaticLine(panel), 0, wx.EXPAND | wx.TOP | wx.BOTTOM, 5)

        # 地址列
        # addrSizer控制所有地址信息，使用gridbag sizer
        addrSizer = wx.GridBagSizer(hgap=5, vgap=5)
        # sizer.Add(bw, pos=(3,0), span=(1,4), flag=wx.EXPAND)
        addrSizer.Add(nameLbl, pos=(0, 0), flag=wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL)
        addrSizer.Add(self.name, pos=(0, 1), flag=wx.EXPAND)
        addrSizer.Add(addrLbl, pos=(1, 0), flag=wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL)
        addrSizer.Add(self.addr1, pos=(1, 1), flag=wx.EXPAND)
        # 带有空白空间的行
        addrSizer.Add(addrLbl2, pos=(2, 0), span=(1, 1),
                      flag=wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL)
        addrSizer.Add(self.addr2, pos=(2, 1), flag=wx.EXPAND)

        addrSizer.Add(projLbl, pos=(3, 0), span=(1, 1),
                      flag=wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL)
        addrSizer.Add(self.proj, pos=(3, 1), flag=wx.EXPAND)

        addrSizer.Add(mavenbl, pos=(4, 0), span=(1, 1),
                      flag=wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL)
        addrSizer.Add(self.maven, pos=(4, 1), flag=wx.EXPAND)

        # 添加几个实际的空白行
        addrSizer.Add((30, 30), pos=(5, 0), span=(1, 2), flag=wx.EXPAND)

        addrSizer.AddGrowableCol(1)
        # 然后把addrSizer添加到mainSizer中
        mainSizer.Add(addrSizer, 0, wx.EXPAND | wx.ALL, 10)

        # 按钮放到两边和中间都能伸缩间隔的一行中
        btnSizer = wx.BoxSizer(wx.HORIZONTAL)
        btnSizer.Add((20, 20), 1)
        btnSizer.Add(saveBtn)
        btnSizer.Add((20, 20), 1)
        btnSizer.Add(cancelBtn)
        btnSizer.Add((20, 20), 1)

        self.Bind(wx.EVT_BUTTON, self.OnUploadMe, saveBtn)
        self.Bind(wx.EVT_BUTTON, self.OnCloseMe, cancelBtn)

        mainSizer.Add(btnSizer, 0, wx.EXPAND | wx.BOTTOM, 10)
        panel.SetSizer(mainSizer)

        # 让框架自适应sizer，如果panel改变大小框架会自动调整尺寸
        # 同时还能防止框架比panel最小尺寸还小
        mainSizer.Fit(self)
        mainSizer.SetSizeHints(self)

        self.Centre()
        self.Show()

    def OnCloseMe(self, event):
        self.Close(True)

    def OnUploadMe(self, event):
        hostname = self.name.GetValue()
        username = self.addr1.GetValue()
        password = self.addr2.GetValue()
        projdir = self.proj.GetValue()
        maven_home = self.maven.GetValue()
        self.ChangeConfig(hostname, username, password, projdir)
        errmsg = ''
        try:
            # 先本地编译
            if not maven_home:
                exe_command = 'cd /d %s && mvn clean && mvn compile' % projdir
            else:
                mvn_full = os.path.join(maven_home, 'bin', 'mvn')
                exe_command = 'cd /d %s && %s clean && %s compile' % (projdir, mvn_full, mvn_full)
            _LOGGING.info('#subprocess exe_command start: %s' % exe_command)
            # 执行命令，但是捕捉输出
            # if os.name == 'nt':
            #     _LOGGING.info('os.name==nt')
            #     startupinfo = subprocess.STARTUPINFO()
            #     startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
            exresult = subprocess_call(exe_command, shell=True)
            # exresult = subprocess_popen(exe_command, shell=True, stdout=subprocess.PIPE)
            # out = exresult.stdout.read()
            # _LOGGING.info(out)
            _LOGGING.info('#subprocess_call result is %s' % exresult)
            _LOGGING.info('#subprocess_call exe_command end')
            if exresult != 0:
                result = False
                errmsg = 'execute maven command failure.'
            else:
                result = ztransfer.main()
        except Exception as e:
            result = False
            errmsg = e.message
        if result:
            _LOGGING.info('MessageDialog.upload.success!!!')
            wx.MessageDialog(self, u'上传成功了！',
                             'MessageDialog', wx.ICON_INFORMATION).ShowModal()
        else:
            _LOGGING.error('MessageDialog.upload.error!!!')
            wx.MessageDialog(self, u'上传失败，error:%s！' % errmsg,
                             'MessageDialog', wx.ICON_INFORMATION).ShowModal()

    def ChangeConfig(self, hostname, username, password, projdir):
        ztransfer.HOSTNAME = hostname
        ztransfer.USERNAME = username
        ztransfer.PASSWORD = password
        ztransfer.DIR_LOCAL = os.path.join(projdir, 'target', 'classes', 'com')
        ztransfer.ZIPDIR_SRC = os.path.join(projdir, 'target', 'classes', 'com')
        ztransfer.ZIPDIR_DEST = projdir


def main():
    # app = wx.App(redirect=True, filename=tempfile.TemporaryFile().name)
    app = wx.App()
    UploadFrame()
    app.MainLoop()
