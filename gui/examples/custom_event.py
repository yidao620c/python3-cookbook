#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
Topic: 创建自定义事件并绑定，两个按钮都点击后才产生事件
Desc : 
"""
import wx


class TwoButtonEvent(wx.PyCommandEvent):
    """先定义一个自定义事件"""

    def __init__(self, evtType, id):
        wx.PyCommandEvent.__init__(self, evtType, id)
        self.clickCount = 0

    def getClickCount(self):
        return self.clickCount

    def setClickCount(self, count):
        self.clickCount = count


EVT_TWO_BUTTON_TYPE = wx.NewEventType()  # 创建一个事件类型
EVT_TWO_BUTTON = wx.PyEventBinder(EVT_TWO_BUTTON_TYPE, 1)  # 创建一个绑定器对象


class TwoButtonPanel(wx.Panel):
    def __init__(self, parent, id=-1, leftText='Left', rightText='Right'):
        wx.Panel.__init__(self, parent, id)
        self.leftButton = wx.Button(self, label=leftText)
        self.rightButton = wx.Button(self, label=rightText, pos=(100, 0))
        self.leftClick = False
        self.rightClick = False
        self.clickCount = 0
        # 4 下面两行绑定更低级的事件
        self.leftButton.Bind(wx.EVT_LEFT_DOWN, self.OnLeftClick)
        self.rightButton.Bind(wx.EVT_LEFT_DOWN, self.OnRightClick)

    def OnLeftClick(self, event):
        self.leftClick = True
        self.OnClick()
        event.Skip()  # 继续处理

    def OnRightClick(self, event):
        self.rightClick = True
        self.OnClick()
        event.Skip()

    def OnClick(self):
        self.clickCount += 1
        if self.leftClick and self.rightClick:
            self.leftClick = False
            self.rightClick = False
            # 创建自定义事件
            myevent = TwoButtonEvent(EVT_TWO_BUTTON_TYPE, self.GetId())
            myevent.setClickCount(self.clickCount)  # 添加数据到事件
            self.GetEventHandler().ProcessEvent(myevent)  # 处理事件


class CustomEventFrame(wx.Frame):
    def __init__(self, parent, id):
        wx.Frame.__init__(self, parent, id, 'Click Count: 0', size=(300, 100))
        panel = TwoButtonPanel(self)
        self.Bind(EVT_TWO_BUTTON, self.OnTwoClick, panel)  # 绑定自定义事件

    def OnTwoClick(self, event):  # 定义一个事件处理器
        self.SetTitle('Click count: %s' % event.getClickCount())


def main():
    app = wx.App()
    frame = CustomEventFrame(parent=None, id=-1)
    frame.Show()
    app.MainLoop()
