#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
    Topic: 简单的一个button，点击关闭窗口
    Desc : 
"""
__author__ = 'Xiong Neng'
import wx


class MyFrame(wx.Frame):
    """Frame class that displays an image"""

    def __init__(self, parent, id):
        """Create a frame instnace and display image"""
        wx.Frame.__init__(self, parent,id,'Frame With Button', size=(300,100))
        panel = wx.Panel(self)  # 创建画板
        # 将按钮添加到画板中去
        button = wx.Button(panel, label='Close', pos=(125, 10), size=(50, 50))
        # 绑定按钮单击事件
        self.Bind(wx.EVT_BUTTON, self.OnCloseMe, button)
        # 绑定窗口关闭事件
        self.Bind(wx.EVT_CLOSE, self.OnCloseWindow)


    def OnCloseMe(self, event):
        self.Close(True)


    def OnCloseWindow(self, event):
        self.Destroy()


class MyApp(wx.App):
    """Application class."""

    def OnInit(self):
        self.frame = MyFrame(parent=None, id=-1)
        self.frame.Show(True)
        self.SetTopWindow(self.frame)
        return True


def main():
    app = MyApp()
    app.MainLoop()

