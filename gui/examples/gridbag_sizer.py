#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
Topic: 布局管理器gridbag sizer
Desc : 
"""
import wx


class BlockWindow(wx.Panel):
    def __init__(self, parent, ID=-1, label='',
                 pos=wx.DefaultPosition, size=(100, 25)):
        wx.Panel.__init__(self, parent, ID, pos, size,
                          wx.RAISED_BORDER, label)
        self.label = label
        self.SetBackgroundColour('white')
        self.SetMinSize(size)
        self.Bind(wx.EVT_PAINT, self.OnPaint)

    def OnPaint(self, evt):
        sz = self.GetClientSize()
        dc = wx.PaintDC(self)
        w, h = dc.GetTextExtent(self.label)
        dc.SetFont(self.GetFont())
        dc.DrawText(self.label, (sz.width - w) / 2, (sz.height - h) / 2)


labels = 'one two three four five six seven eight nine'.split()


class GridbagFrame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, -1, 'GridBagSizer')
        sizer = wx.GridBagSizer(hgap=5, vgap=5)
        for col in range(3):
            for row in range(3):
                bw = BlockWindow(self, label=labels[row * 3 + col])
                sizer.Add(bw, pos=(row, col))

        # 跨行
        bw = BlockWindow(self, label='span 3 rows')
        sizer.Add(bw, pos=(0, 3), span=(3, 1), flag=wx.EXPAND)
        # 跨列
        bw = BlockWindow(self, label='span all columns')
        sizer.Add(bw, pos=(3, 0), span=(1, 4), flag=wx.EXPAND)
        # 使最后的行和列可增加
        sizer.AddGrowableCol(3)
        sizer.AddGrowableRow(3)
        self.SetSizer(sizer)
        self.Fit()


def main():
    app = wx.App()
    GridbagFrame().Show()
    app.MainLoop()



