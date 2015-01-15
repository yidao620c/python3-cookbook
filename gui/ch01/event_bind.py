#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
Topic: 事件绑定示例
Desc : 
"""
import wx


class MouseEventFrame(wx.Frame):
    def __init__(self, parent, id):
        wx.Frame.__init__(self, parent, id, 'Show Event Bindings', size=(300, 100))
        self.panel = wx.Panel(self)
        self.button = wx.Button(self.panel, label='Not Over', pos=(100, 15))
        self.Bind(wx.EVT_BUTTON, self.OnButtonClick, self.button)  # 绑定button点击事件
        self.button.Bind(wx.EVT_ENTER_WINDOW, self.OnEnterWindow)  # 光标位于其上事件
        self.button.Bind(wx.EVT_LEAVE_WINDOW, self.OnLeaveWindow)  # 光标离开事件

    def OnButtonClick(self, event):
        self.panel.SetBackgroundColour('Green')
        self.panel.Refresh()

    def OnEnterWindow(self, event):
        self.button.SetLabel('Over Me!')
        event.Skip()

    def OnLeaveWindow(self, event):
        self.button.SetLabel('Not Over')
        event.Skip()

class DoubleEventFrame(wx.Frame):
    """同时监听两个事件"""
    def __init__(self, parent, id):
        wx.Frame.__init__(self, parent, id, 'Show Event Bindings', size=(300, 100))
        self.panel = wx.Panel(self)
        self.button = wx.Button(self.panel, label='Not Over', pos=(100, 15))
        self.Bind(wx.EVT_BUTTON, self.OnButtonClick, self.button)  # 绑定button点击事件
        self.button.Bind(wx.EVT_LEFT_DOWN, self.OnMouseDown)  # 鼠标左键点击

    def OnButtonClick(self, event):
        """鼠标点击后释放才会有这个Click事件"""
        self.panel.SetBackgroundColour('Green')
        self.panel.Refresh()

    def OnMouseDown(self, event):
        self.button.SetLabel('Over Me!')
        event.Skip()  # 鼠标左键事件会优先产生，这时候Skip()会继续去传递这个事件

def main():
    app = wx.App()
    # frame = MouseEventFrame(parent=None, id=-1)
    frame = DoubleEventFrame(parent=None, id=-1)
    frame.Show()
    app.MainLoop()

