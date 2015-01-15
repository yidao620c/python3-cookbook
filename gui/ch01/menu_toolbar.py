#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
    Topic: 菜单栏、工具栏、状态栏
    Desc : 
"""
__author__ = 'Xiong Neng'
import wx
import wx.py.images as images


class MenuToobarFrame(wx.Frame):
    """Frame class that displays an image"""

    def __init__(self, parent, id):
        """Create a frame instnace and display image"""
        wx.Frame.__init__(self, parent,id,'Toolbars', size=(300, 200))
        panel = wx.Panel(self)  # 创建画板
        panel.SetBackgroundColour('White')
        statusBar = self.CreateStatusBar()  # 创建状态栏
        toolbar = self.CreateToolBar()  # 创建工具栏
        # 给工具栏增加一个工具
        toolbar.AddSimpleTool(wx.NewId(), images.getPyBitmap(), 'New', "Long help for 'New'")
        toolbar.Realize()  # 准备显示工具栏
        menuBar = wx.MenuBar()  # 创建一个菜单栏
        # 创建两个菜单
        menu1 = wx.Menu()
        menuBar.Append(menu1, '&File')
        menu1.Append(-1, "&Open...", 'Open new file')
        menuItem = menu1.Append(-1, "&Exit...", 'Exit System')
        # 菜单项绑定事件
        self.Bind(wx.EVT_MENU, self.OnCloseMe, menuItem)
        menu2 = wx.Menu()
        # 创建菜单项MenuItem
        menu2.Append(wx.NewId(), '&Copy', 'Copy in status bar')
        menu2.Append(wx.NewId(), '&Cut', '')
        menu2.Append(wx.NewId(), '&Paste','')
        menu2.AppendSeparator()
        menu2.Append(wx.NewId(), '&Options', 'Display Options')
        menuBar.Append(menu2, '&Edit')  # 在菜单栏上附上菜单
        self.SetMenuBar(menuBar)  # 在Frame上面附加菜单

    def OnCloseMe(self, event):
        self.Close(True)


def main():
    app = wx.App()
    frame = MenuToobarFrame(parent=None, id=-1)
    frame.Show()
    app.MainLoop()

