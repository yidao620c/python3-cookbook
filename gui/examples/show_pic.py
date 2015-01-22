#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
    Topic: 显示一张图片
    Desc : 
"""
__author__ = 'Xiong Neng'
import wx
import commons.util as util


class MyFrame(wx.Frame):
    """Frame class that displays an image"""

    def __init__(self, image, parent=None, id=-1,
                 pos=wx.DefaultPosition,
                 title='Hello, wxPython!'):
        """Create a frame instnace and display image"""
        temp = image.ConvertToBitmap()
        size = temp.GetWidth(), temp.GetHeight()
        wx.Frame.__init__(self, parent, id, title, pos, size)
        self.bmp = wx.StaticBitmap(parent=self, bitmap=temp)


class MyApp(wx.App):
    """Application class."""

    def OnInit(self):
        img = wx.Image(util.resource_path('resources/f22.jpg'), wx.BITMAP_TYPE_JPEG)
        self.frame = MyFrame(image=img)
        self.frame.Show(True)
        self.SetTopWindow(self.frame)
        return True


def main():
    app = MyApp()
    app.MainLoop()

