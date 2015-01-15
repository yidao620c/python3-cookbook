#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
    Topic: 显示鼠标的位置
    Desc : 
"""
import wx
__author__ = 'Xiong Neng'


class MyFrame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, -1, "My Frame", size=(300, 300))
        panel = wx.Panel(self, -1)
        panel.Bind(wx.EVT_MOTION, self.OnMove)
        wx.StaticText(panel, -1, 'Pos: ', pos=(40, 10))
        self.posCtrl = wx.TextCtrl(panel, -1, '', pos=(40, 10))

    def OnMove(self, event):
        pos = event.GetPosition()
        self.posCtrl.SetValue('%s, %s' % (pos.x, pos.y))


def main():
    app = wx.App()
    frame = MyFrame()
    frame.Show(True)
    app.MainLoop()
