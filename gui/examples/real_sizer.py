#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
Topic: 真实form表单sizer，复杂度适中
Desc : 
"""
import wx


class FormFrame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, -1, 'Real World')
        panel = wx.Panel(self)
        # 首先创建controls
        topLbl = wx.StaticText(panel, -1, 'Account Information')
        topLbl.SetFont(wx.Font(18, wx.SWISS, wx.NORMAL, wx.BOLD))
        nameLbl = wx.StaticText(panel, -1, 'Name:')
        name = wx.TextCtrl(panel, -1, '')  # 文本输入框
        addrLbl = wx.StaticText(panel, -1, 'Address:')
        addr1 = wx.TextCtrl(panel, -1, '')
        addr2 = wx.TextCtrl(panel, -1, '')
        cstLbl = wx.StaticText(panel, -1, 'City,State,Zip:')
        city = wx.TextCtrl(panel, -1, '', size=(150, -1))
        state = wx.TextCtrl(panel, -1, '', size=(50, -1))
        zip = wx.TextCtrl(panel, -1, '', size=(70, -1))
        phoneLbl = wx.StaticText(panel, -1, 'Phone:')
        phone = wx.TextCtrl(panel, -1, '')
        emailLbl = wx.StaticText(panel, -1, 'Email:')
        email = wx.TextCtrl(panel, -1, '')
        saveBtn = wx.Button(panel, -1, 'Save')
        cancelBtn = wx.Button(panel, -1, 'Cancel')

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
        addrSizer.Add(name, pos=(0, 1), flag=wx.EXPAND)
        addrSizer.Add(addrLbl, pos=(1, 0), flag=wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL)
        addrSizer.Add(addr1, pos=(1, 1), flag=wx.EXPAND)
        # 带有空白空间的行
        addrSizer.Add((10, 10), pos=(2, 0), span=(1, 1), flag=wx.EXPAND)  # 一些空白空间
        addrSizer.Add(addr2, pos=(2, 1), flag=wx.EXPAND)
        addrSizer.Add(cstLbl, pos=(3, 0), flag=wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL)

        # city,state,zip放到一个嵌套sizer中，使用BoxSizer
        # 水平嵌套Sizer
        cstSizer = wx.BoxSizer(wx.HORIZONTAL)
        cstSizer.Add(city, 1)
        cstSizer.Add(state, 0, wx.LEFT | wx.RIGHT, 5)
        cstSizer.Add(zip)
        # 把cstSizer加入到addrSizer中
        addrSizer.Add(cstSizer, pos=(3, 1), span=(1, 1), flag=wx.EXPAND)

        # 电话和电子邮箱
        addrSizer.Add(phoneLbl, pos=(4, 0), flag=wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL)
        addrSizer.Add(phone, pos=(4, 1), flag=wx.EXPAND)
        addrSizer.Add(emailLbl, pos=(5, 0), flag=wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL)
        addrSizer.Add(email, pos=(5, 1), flag=wx.EXPAND)

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

        mainSizer.Add(btnSizer, 0, wx.EXPAND | wx.BOTTOM, 10)
        panel.SetSizer(mainSizer)

        # 让框架自适应sizer，如果panel改变大小框架会自动调整尺寸
        # 同时还能防止框架比panel最小尺寸还小
        mainSizer.Fit(self)
        mainSizer.SetSizeHints(self)

        self.Centre()
        self.Show()


def main():
    app = wx.App()
    FormFrame()
    app.MainLoop()



